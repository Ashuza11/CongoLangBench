"""Run one non-Gemma local model over its valid frozen benchmark scope.

Designed for resumable Kaggle GPU sessions. Causal instruction models evaluate
all 47 tracks. Translation-specific models evaluate only exact, validated model
language tags and write a coverage manifest alongside their private predictions.
"""
from __future__ import annotations

import argparse
import csv
import json
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from run_gemma_full import append_jsonl, load_tracks, read_jsonl


BENCHMARK_VERSION = "v1"
PROMPT_VERSION = "translation_v1"
NLLB_CODES = {
    "lin": "lin_Latn",
    "lua": "lua_Latn",
    "bem": "bem_Latn",
    "kon": "kon_Latn",
}
REFERENCE_NLLB_CODES = {"English": "eng_Latn", "French": "fra_Latn"}
MADLAD_CODE_OVERRIDES = {"lin": "ln", "kon": "kg"}
REFERENCE_MADLAD_CODES = {"English": "en", "French": "fr"}
PROFILES = {
    "apertus": {
        "model_id": "swiss-ai/Apertus-8B-Instruct-2509",
        "backend": "chat_causal",
        "precision": "4bit",
        "licence": "Apache-2.0",
    },
    "madlad": {
        "model_id": "google/madlad400-10b-mt",
        "backend": "madlad",
        "precision": "4bit",
        "licence": "Apache-2.0",
    },
    "nllb": {
        "model_id": "facebook/nllb-200-3.3B",
        "backend": "nllb",
        "precision": "fp16",
        "licence": "CC-BY-NC-4.0",
    },
    "bloomz": {
        "model_id": "bigscience/bloomz-7b1-mt",
        "backend": "plain_causal",
        "precision": "4bit",
        "licence": "BigScience-BLOOM-RAIL-1.0",
    },
}


def prediction_key(row: dict) -> tuple[str, str, str]:
    return row["iso_code"], row["direction"], row["record_id"]


def validate_resume(rows: list[dict], model_id: str) -> dict[tuple[str, str, str], dict]:
    completed = {}
    for row in rows:
        if row.get("model_id") != model_id:
            raise ValueError("Resume file contains a different model")
        if row.get("benchmark_version") != BENCHMARK_VERSION:
            raise ValueError("Resume file contains a different benchmark version")
        row_key = prediction_key(row)
        if row_key in completed:
            raise ValueError(f"Duplicate resume key: {row_key}")
        completed[row_key] = row
    return completed


def madlad_tag_exists(tokenizer, code: str) -> bool:
    token = f"<2{code}>"
    token_id = tokenizer.convert_tokens_to_ids(token)
    return token_id is not None and token_id != tokenizer.unk_token_id


def build_jobs(
    repo_root: Path,
    data_root: Path,
    tracks: list[dict[str, str]],
    backend: str,
    tokenizer,
) -> tuple[list[dict], list[dict]]:
    prompt_template = (
        repo_root / "evaluations/prompts/translation_v1.txt"
    ).read_text(encoding="utf-8").strip()
    jobs = []
    coverage = []
    for track in tracks:
        if backend == "nllb":
            target_code = NLLB_CODES.get(track["iso_code"])
            supported = bool(target_code)
            detail = target_code or "no exact FLORES-200/NLLB code"
        elif backend == "madlad":
            candidate = MADLAD_CODE_OVERRIDES.get(track["iso_code"], track["iso_code"])
            supported = madlad_tag_exists(tokenizer, candidate)
            target_code = candidate if supported else None
            detail = f"<2{candidate}>" if supported else f"<2{candidate}> absent from tokenizer"
        else:
            supported = True
            target_code = None
            detail = "zero-shot instruction evaluation"
        coverage.append(
            {
                "language": track["language"],
                "iso_code": track["iso_code"],
                "supported": supported,
                "model_language_code": target_code,
                "detail": detail,
            }
        )
        if not supported:
            continue
        with (data_root / track["benchmark_csv"]).open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 1500:
            raise ValueError(f"Expected 1,500 rows for {track['iso_code']}")
        for direction in ("reference_to_congolese", "congolese_to_reference"):
            if direction == "reference_to_congolese":
                source_column, reference_column = "source_text", "target_text"
                source_language, target_language = track["reference_language"], track["language"]
                if backend == "nllb":
                    source_tag = REFERENCE_NLLB_CODES[track["reference_language"]]
                    target_tag = target_code
                elif backend == "madlad":
                    source_tag = REFERENCE_MADLAD_CODES[track["reference_language"]]
                    target_tag = target_code
            else:
                source_column, reference_column = "target_text", "source_text"
                source_language, target_language = track["language"], track["reference_language"]
                if backend == "nllb":
                    source_tag = target_code
                    target_tag = REFERENCE_NLLB_CODES[track["reference_language"]]
                elif backend == "madlad":
                    source_tag = target_code
                    target_tag = REFERENCE_MADLAD_CODES[track["reference_language"]]
            for row in rows:
                source_text = row[source_column]
                job = {
                    "language": track["language"],
                    "iso_code": track["iso_code"],
                    "direction": direction,
                    "record_id": row["record_id"],
                    "source_text": source_text,
                    "reference_text": row[reference_column],
                    "source_language": source_language,
                    "target_language": target_language,
                }
                if backend in {"chat_causal", "plain_causal"}:
                    job["model_input"] = prompt_template.format(
                        source_language=source_language,
                        target_language=target_language,
                        input_text=source_text,
                    )
                else:
                    job["source_tag"] = source_tag
                    job["target_tag"] = target_tag
                    if backend == "madlad":
                        job["model_input"] = f"<2{target_tag}> {source_text}"
                jobs.append(job)
    return jobs, coverage


def trim(ids, eos_id: int | None, pad_id: int | None) -> list[int]:
    values = ids.tolist()
    if eos_id is not None and eos_id in values:
        values = values[: values.index(eos_id) + 1]
    while values and pad_id is not None and values[-1] == pad_id:
        values.pop()
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-key", choices=sorted(PROFILES), required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--resume-predictions", type=Path)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--retry-max-new-tokens", type=int, default=768)
    parser.add_argument(
        "--max-runtime-minutes",
        type=int,
        default=600,
        help="Stop cleanly after this much inference time so Kaggle can save outputs",
    )
    args = parser.parse_args()

    import torch
    from transformers import (
        AutoModelForCausalLM,
        AutoModelForSeq2SeqLM,
        AutoTokenizer,
        BitsAndBytesConfig,
    )

    if not torch.cuda.is_available():
        raise RuntimeError("A CUDA GPU is required")
    profile = PROFILES[args.model_key]
    model_id = profile["model_id"]
    backend = profile["backend"]
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    predictions_path = output_root / "predictions.jsonl"
    if args.resume_predictions and not predictions_path.exists():
        predictions_path.write_bytes(args.resume_predictions.read_bytes())

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.padding_side = "left" if "causal" in backend else "right"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    tracks = load_tracks(args.repo_root.resolve(), args.data_root.resolve())
    jobs, coverage = build_jobs(
        args.repo_root.resolve(), args.data_root.resolve(), tracks, backend, tokenizer
    )
    (output_root / "coverage.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    supported_count = sum(row["supported"] for row in coverage)
    print(f"Coverage: {supported_count}/47 tracks; {len(jobs):,} production requests.")

    compute_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    load_kwargs = {"device_map": "auto", "low_cpu_mem_usage": True, "dtype": compute_dtype}
    if profile["precision"] == "4bit":
        load_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=compute_dtype,
        )
    model_class = AutoModelForCausalLM if "causal" in backend else AutoModelForSeq2SeqLM
    model = model_class.from_pretrained(model_id, **load_kwargs)
    model.eval()
    revision = getattr(model.config, "_commit_hash", None)

    completed = validate_resume(read_jsonl(predictions_path), model_id)
    resumed_revisions = {row.get("model_revision") for row in completed.values()}
    if completed and resumed_revisions != {revision}:
        raise ValueError(
            f"Checkpoint model revision {resumed_revisions} does not match loaded revision {revision}"
        )
    expected_keys = {prediction_key(job) for job in jobs}
    extras = set(completed) - expected_keys
    if extras:
        raise ValueError(f"Resume file contains {len(extras)} out-of-scope records")
    pending = [job for job in jobs if prediction_key(job) not in completed]
    pending.sort(
        key=lambda job: (
            job.get("source_tag", ""),
            job.get("target_tag", ""),
            len(job.get("model_input", job["source_text"])),
        )
    )
    print(f"Resuming with {len(completed):,}/{len(jobs):,} complete.")
    gpu = torch.cuda.get_device_properties(0)
    session_started = time.perf_counter()
    generated_this_session = 0

    def infer(batch: list[dict], limit: int) -> list[dict]:
        nonlocal generated_this_session
        if backend == "chat_causal":
            texts = [
                tokenizer.apply_chat_template(
                    [{"role": "user", "content": job["model_input"]}],
                    tokenize=False,
                    add_generation_prompt=True,
                )
                for job in batch
            ]
        elif backend == "plain_causal":
            texts = [job["model_input"] for job in batch]
        elif backend == "madlad":
            texts = [job["model_input"] for job in batch]
        else:
            if len({job["source_tag"] for job in batch}) != 1 or len(
                {job["target_tag"] for job in batch}
            ) != 1:
                raise ValueError("NLLB batches must share source and target tags")
            tokenizer.src_lang = batch[0]["source_tag"]
            texts = [job["source_text"] for job in batch]
        encoded = tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(
            model.device
        )
        generate_kwargs = {
            "do_sample": False,
            "max_new_tokens": limit,
            "pad_token_id": tokenizer.pad_token_id,
        }
        if backend == "nllb":
            generate_kwargs["forced_bos_token_id"] = tokenizer.convert_tokens_to_ids(
                batch[0]["target_tag"]
            )
        started = time.perf_counter()
        try:
            with torch.inference_mode():
                generated = model.generate(**encoded, **generate_kwargs)
        except torch.OutOfMemoryError:
            del encoded
            torch.cuda.empty_cache()
            if len(batch) == 1:
                raise
            midpoint = len(batch) // 2
            print(f"OOM at {len(batch)} rows; splitting the production batch.")
            return infer(batch[:midpoint], limit) + infer(batch[midpoint:], limit)
        elapsed = time.perf_counter() - started
        prefix = encoded["input_ids"].shape[-1] if "causal" in backend else 0
        results = []
        for job, sequence, attention in zip(batch, generated, encoded["attention_mask"]):
            output_ids = trim(sequence[prefix:], tokenizer.eos_token_id, tokenizer.pad_token_id)
            token_count = len(output_ids)
            results.append(
                {
                    "model_id": model_id,
                    "model_revision": revision,
                    "model_key": args.model_key,
                    "model_licence": profile["licence"],
                    "benchmark_version": BENCHMARK_VERSION,
                    "prompt_version": PROMPT_VERSION if "causal" in backend else None,
                    "iso_code": job["iso_code"],
                    "language": job["language"],
                    "direction": job["direction"],
                    "record_id": job["record_id"],
                    "source_tag": job.get("source_tag"),
                    "target_tag": job.get("target_tag"),
                    "prediction": tokenizer.decode(output_ids, skip_special_tokens=True).strip(),
                    "input_tokens": int(attention.sum().item()),
                    "generated_tokens": token_count,
                    "max_new_tokens_used": limit,
                    "finish_reason": "length" if token_count >= limit else "stop",
                    "batch_size": len(batch),
                    "batch_elapsed_seconds": round(elapsed, 3),
                }
            )
        generated_this_session += len(results)
        return results

    cursor = 0
    while cursor < len(pending):
        group = pending[cursor : cursor + args.batch_size]
        if backend == "nllb":
            pair = (group[0]["source_tag"], group[0]["target_tag"])
            group = [job for job in group if (job["source_tag"], job["target_tag"]) == pair]
        results = infer(group, args.max_new_tokens)
        capped_positions = [i for i, result in enumerate(results) if result["finish_reason"] == "length"]
        if capped_positions:
            retry_jobs = [group[i] for i in capped_positions]
            retry_results = infer(retry_jobs, args.retry_max_new_tokens)
            replacements = {prediction_key(row): row for row in retry_results}
            results = [replacements.get(prediction_key(row), row) for row in results]
        append_jsonl(predictions_path, results)
        completed.update((prediction_key(row), row) for row in results)
        cursor += len(group)
        if generated_this_session % 100 < len(group):
            rate = generated_this_session / max(time.perf_counter() - session_started, 1)
            print(f"{len(completed):,}/{len(jobs):,} complete | {rate:.2f} records/s")

        elapsed_minutes = (time.perf_counter() - session_started) / 60
        if elapsed_minutes >= args.max_runtime_minutes:
            session_state = {
                "model_id": model_id,
                "benchmark_version": BENCHMARK_VERSION,
                "complete": len(completed),
                "expected": len(jobs),
                "remaining": len(jobs) - len(completed),
                "stopped_cleanly_for_kaggle_save": True,
                "updated_at_utc": datetime.now(timezone.utc).isoformat(),
            }
            (output_root / "session_state.json").write_text(
                json.dumps(session_state, indent=2) + "\n", encoding="utf-8"
            )
            print(json.dumps(session_state, indent=2))
            return

    missing = expected_keys - set(completed)
    if missing:
        raise RuntimeError(f"Run ended with {len(missing):,} missing predictions")
    rows = list(completed.values())
    metadata = {
        "run_type": "full_supported_scope",
        "model_key": args.model_key,
        "model_id": model_id,
        "model_revision": revision,
        "model_licence": profile["licence"],
        "repository_commit": subprocess.check_output(
            ["git", "-C", str(args.repo_root), "rev-parse", "HEAD"], text=True
        ).strip(),
        "benchmark_version": BENCHMARK_VERSION,
        "prompt_version": PROMPT_VERSION if "causal" in backend else None,
        "supported_language_tracks": supported_count,
        "total_language_tracks": 47,
        "requests": len(rows),
        "empty_predictions": sum(not row["prediction"] for row in rows),
        "remaining_truncations": sum(row["finish_reason"] == "length" for row in rows),
        "precision": profile["precision"],
        "initial_max_new_tokens": args.max_new_tokens,
        "truncation_retry_max_new_tokens": args.retry_max_new_tokens,
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
