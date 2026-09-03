"""Run the complete frozen benchmark with Gemma using resumable GPU batches.

The benchmark text and predictions may be licence-restricted. Point ``--data-root``
and ``--output-root`` at private storage; this script never uploads either one.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


MODEL_ID = "google/gemma-4-12B-it"
BENCHMARK_VERSION = "v1"
PROMPT_VERSION = "translation_v1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def append_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        handle.flush()


def load_tracks(repo_root: Path, data_root: Path) -> list[dict[str, str]]:
    tracked = repo_root / "registry/benchmark_freeze.csv"
    private = data_root / "registry/benchmark_freeze.csv"
    if not tracked.is_file() or not private.is_file():
        raise FileNotFoundError("The tracked and private freeze manifests are required")
    if sha256(tracked) != sha256(private):
        raise ValueError("Private manifest does not match this repository revision")
    with private.open(encoding="utf-8-sig", newline="") as handle:
        tracks = list(csv.DictReader(handle))
    if len(tracks) != 47:
        raise ValueError(f"Expected 47 frozen tracks; found {len(tracks)}")
    for track in tracks:
        benchmark = data_root / track["benchmark_csv"]
        if not benchmark.is_file():
            raise FileNotFoundError(f"Missing benchmark for {track['iso_code']}: {benchmark}")
        if sha256(benchmark) != track["benchmark_sha256"]:
            raise ValueError(f"Checksum mismatch for {track['iso_code']}")
        if int(track["benchmark_pairs"]) != 1500:
            raise ValueError(f"Expected 1,500 pairs for {track['iso_code']}")
    return tracks


def build_jobs(repo_root: Path, data_root: Path, tracks: list[dict[str, str]]) -> list[dict]:
    prompt_template = (
        repo_root / "evaluations/prompts/translation_v1.txt"
    ).read_text(encoding="utf-8").strip()
    jobs: list[dict] = []
    for track in tracks:
        with (data_root / track["benchmark_csv"]).open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 1500:
            raise ValueError(f"Expected 1,500 rows for {track['iso_code']}; found {len(rows)}")
        for direction in ("reference_to_congolese", "congolese_to_reference"):
            for row in rows:
                if direction == "reference_to_congolese":
                    source_text, reference_text = row["source_text"], row["target_text"]
                    source_language, target_language = track["reference_language"], track["language"]
                else:
                    source_text, reference_text = row["target_text"], row["source_text"]
                    source_language, target_language = track["language"], track["reference_language"]
                prompt = prompt_template.format(
                    source_language=source_language,
                    target_language=target_language,
                    input_text=source_text,
                )
                jobs.append(
                    {
                        "language": track["language"],
                        "iso_code": track["iso_code"],
                        "direction": direction,
                        "record_id": row["record_id"],
                        "reference_text": reference_text,
                        "prompt": prompt,
                    }
                )
    if len(jobs) != 141_000:
        raise ValueError(f"Expected 141,000 requests; prepared {len(jobs):,}")
    return jobs


def key(row: dict) -> tuple[str, str, str]:
    return row["iso_code"], row["direction"], row["record_id"]


def validate_resume(rows: list[dict]) -> dict[tuple[str, str, str], dict]:
    completed: dict[tuple[str, str, str], dict] = {}
    for row in rows:
        if row.get("model_id") != MODEL_ID:
            raise ValueError("Existing output contains a different model")
        if row.get("benchmark_version") != BENCHMARK_VERSION:
            raise ValueError("Existing output contains a different benchmark version")
        if row.get("prompt_version") != PROMPT_VERSION:
            raise ValueError("Existing output contains a different prompt version")
        row_key = key(row)
        if row_key in completed:
            raise ValueError(f"Duplicate existing prediction: {row_key}")
        completed[row_key] = row
    return completed


def trim_generated(ids, eos_id: int | None, pad_id: int | None) -> list[int]:
    values = ids.tolist()
    if eos_id is not None and eos_id in values:
        values = values[: values.index(eos_id) + 1]
    while values and pad_id is not None and values[-1] == pad_id:
        values.pop()
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--retry-max-new-tokens", type=int, default=768)
    args = parser.parse_args()
    if args.batch_size < 1:
        raise ValueError("batch-size must be positive")
    if args.retry_max_new_tokens <= args.max_new_tokens:
        raise ValueError("retry limit must be greater than the initial token limit")

    import torch
    from transformers import AutoModelForMultimodalLM, AutoProcessor, BitsAndBytesConfig

    if not torch.cuda.is_available():
        raise RuntimeError("A CUDA GPU is required")

    repo_root = args.repo_root.resolve()
    data_root = args.data_root.resolve()
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    predictions_path = output_root / "predictions.jsonl"
    tracks = load_tracks(repo_root, data_root)
    jobs = build_jobs(repo_root, data_root, tracks)
    completed = validate_resume(read_jsonl(predictions_path))
    expected_keys = {key(job) for job in jobs}
    extras = set(completed) - expected_keys
    if extras:
        raise ValueError(f"Existing output contains {len(extras)} unexpected record keys")
    pending = [job for job in jobs if key(job) not in completed]
    # Adjacent similar lengths reduce padding without changing record identity.
    pending.sort(key=lambda job: len(job["prompt"]))
    print(f"Validated 47 tracks and 141,000 requests; resuming at {len(completed):,} complete.")

    compute_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    quantization = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=compute_dtype,
    )
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    tokenizer = processor.tokenizer
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForMultimodalLM.from_pretrained(
        MODEL_ID,
        quantization_config=quantization,
        device_map="auto",
        dtype=compute_dtype,
        low_cpu_mem_usage=True,
    )
    model.eval()
    revision = getattr(model.config, "_commit_hash", None)
    resumed_revisions = {row.get("model_revision") for row in completed.values()}
    if completed and resumed_revisions != {revision}:
        raise ValueError(
            f"Checkpoint model revision {resumed_revisions} does not match loaded revision {revision}"
        )
    gpu = torch.cuda.get_device_properties(0)
    print(f"Loaded {MODEL_ID} revision={revision} on {gpu.name}.")

    started_run = time.perf_counter()
    generated_this_run = 0

    def generate_batch(batch: list[dict], max_new_tokens: int) -> list[dict]:
        nonlocal generated_this_run
        messages = [[{"role": "user", "content": job["prompt"]}] for job in batch]
        rendered = [
            processor.apply_chat_template(
                message,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            )
            for message in messages
        ]
        inputs = processor(
            text=rendered,
            padding=True,
            return_tensors="pt",
            add_special_tokens=False,
        ).to(model.device)
        input_width = inputs["input_ids"].shape[-1]
        batch_started = time.perf_counter()
        try:
            with torch.inference_mode():
                generated = model.generate(
                    **inputs,
                    do_sample=False,
                    max_new_tokens=max_new_tokens,
                    pad_token_id=tokenizer.pad_token_id,
                )
        except torch.OutOfMemoryError:
            del inputs
            torch.cuda.empty_cache()
            if len(batch) == 1:
                raise
            midpoint = len(batch) // 2
            print(f"OOM at batch {len(batch)}; retrying as {midpoint}+{len(batch)-midpoint}.")
            return generate_batch(batch[:midpoint], max_new_tokens) + generate_batch(
                batch[midpoint:], max_new_tokens
            )
        elapsed = time.perf_counter() - batch_started
        results = []
        for job, sequence, attention in zip(batch, generated, inputs["attention_mask"]):
            output_ids = trim_generated(
                sequence[input_width:], tokenizer.eos_token_id, tokenizer.pad_token_id
            )
            token_count = len(output_ids)
            hit_limit = token_count >= max_new_tokens
            prediction = tokenizer.decode(output_ids, skip_special_tokens=True).strip()
            results.append(
                {
                    "model_id": MODEL_ID,
                    "model_revision": revision,
                    "benchmark_version": BENCHMARK_VERSION,
                    "prompt_version": PROMPT_VERSION,
                    "iso_code": job["iso_code"],
                    "language": job["language"],
                    "direction": job["direction"],
                    "record_id": job["record_id"],
                    "prediction": prediction,
                    "input_tokens": int(attention.sum().item()),
                    "generated_tokens": token_count,
                    "max_new_tokens_used": max_new_tokens,
                    "finish_reason": "length" if hit_limit else "stop",
                    "batch_size": len(batch),
                    "batch_elapsed_seconds": round(elapsed, 3),
                }
            )
        generated_this_run += len(results)
        return results

    cursor = 0
    while cursor < len(pending):
        batch = pending[cursor : cursor + args.batch_size]
        results = generate_batch(batch, args.max_new_tokens)
        capped = [result for result in results if result["finish_reason"] == "length"]
        if capped:
            retry_jobs = [batch[results.index(result)] for result in capped]
            retry_results = generate_batch(retry_jobs, args.retry_max_new_tokens)
            replacements = {key(result): result for result in retry_results}
            results = [replacements.get(key(result), result) for result in results]
        append_jsonl(predictions_path, results)
        completed.update((key(result), result) for result in results)
        cursor += len(batch)
        if generated_this_run % 100 < len(batch):
            elapsed_hours = (time.perf_counter() - started_run) / 3600
            rate = generated_this_run / max(time.perf_counter() - started_run, 1)
            print(
                f"{len(completed):,}/141,000 complete | {rate:.2f} records/s | "
                f"{elapsed_hours:.2f} h this session"
            )

    missing = expected_keys - set(completed)
    if missing:
        raise RuntimeError(f"Run ended with {len(missing):,} missing predictions")
    final_rows = list(completed.values())
    empty = sum(not row["prediction"].strip() for row in final_rows)
    capped = sum(row["finish_reason"] == "length" for row in final_rows)
    metadata = {
        "run_type": "full_benchmark",
        "model_id": MODEL_ID,
        "model_revision": revision,
        "repository_commit": subprocess.check_output(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True
        ).strip(),
        "benchmark_version": BENCHMARK_VERSION,
        "prompt_version": PROMPT_VERSION,
        "language_tracks": 47,
        "directions": 2,
        "rows_per_direction": 1500,
        "requests": len(final_rows),
        "empty_predictions": empty,
        "remaining_truncations": capped,
        "do_sample": False,
        "thinking_enabled": False,
        "initial_max_new_tokens": args.max_new_tokens,
        "truncation_retry_max_new_tokens": args.retry_max_new_tokens,
        "quantization": "bitsandbytes_nf4_4bit",
        "gpu": gpu.name,
        "gpu_memory_gib": round(gpu.total_memory / 2**30, 2),
        "python_version": platform.python_version(),
        "torch_version": torch.__version__,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "contains_model_outputs_from_restricted_inputs": True,
    }
    (output_root / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
