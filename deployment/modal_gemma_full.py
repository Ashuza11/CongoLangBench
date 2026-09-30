"""Resume the private Gemma benchmark on a budget-capped Modal L40S job.

Run this file only through the Modal CLI. Private benchmark text and predictions
are uploaded to a named private Volume and are never included in the image.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
import zipfile
from contextlib import ExitStack
from pathlib import Path

import modal


LOCAL_ROOT = Path(__file__).resolve().parents[1]
REMOTE_ROOT = Path("/opt/CongoLangBench")
VOLUME_ROOT = Path("/private")
BENCHMARK_ZIP = VOLUME_ROOT / "input/congolang-benchmark-v1.zip"
DATA_ROOT = VOLUME_ROOT / "benchmark-v1"
RUN_ROOT = VOLUME_ROOT / "runs/gemma4-12b-it-full-v1"
PREDICTIONS = RUN_ROOT / "predictions.jsonl"
VOLUME_NAME = "congolang-benchmark-private"
MODEL_CACHE_NAME = "congolang-huggingface-cache"

REPOSITORY_COMMIT = subprocess.check_output(
    ["git", "-C", str(LOCAL_ROOT), "rev-parse", "HEAD"], text=True
).strip()

image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.8.1-cudnn-runtime-ubuntu22.04", add_python="3.12"
    )
    .pip_install(
        "torch==2.11.0",
        "transformers>=5,<6",
        "accelerate",
        "bitsandbytes",
        "huggingface_hub",
        "sacrebleu",
        "pandas==2.2.3",
    )
    .add_local_dir(LOCAL_ROOT / "scripts", str(REMOTE_ROOT / "scripts"), copy=True)
    .add_local_dir(LOCAL_ROOT / "registry", str(REMOTE_ROOT / "registry"), copy=True)
    .add_local_dir(
        LOCAL_ROOT / "evaluations/prompts",
        str(REMOTE_ROOT / "evaluations/prompts"),
        copy=True,
    )
)

app = modal.App("congolang-gemma-full")
private_volume = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)
model_cache = modal.Volume.from_name(MODEL_CACHE_NAME, create_if_missing=True)
hf_secret = modal.Secret.from_name("congolang-huggingface", required_keys=["HF_TOKEN"])


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


@app.function(
    image=image,
    gpu="L40S",
    cpu=2,
    memory=32_768,
    timeout=11 * 60 * 60,
    volumes={
        str(VOLUME_ROOT): private_volume,
        "/root/.cache/huggingface": model_cache,
    },
    secrets=[hf_secret],
)
def run_gemma(batch_size: int = 32, max_runtime_minutes: int = 600) -> dict:
    """Run production inference for at most 10 hours of the 11-hour container."""
    import os
    import zipfile

    if not BENCHMARK_ZIP.is_file():
        raise FileNotFoundError(
            f"{BENCHMARK_ZIP} is absent; run the upload action before paid inference"
        )
    private_manifest = DATA_ROOT / "registry/benchmark_freeze.csv"
    if not private_manifest.is_file():
        DATA_ROOT.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(BENCHMARK_ZIP) as archive:
            for member in archive.infolist():
                destination = (DATA_ROOT / member.filename).resolve()
                if not destination.is_relative_to(DATA_ROOT.resolve()):
                    raise ValueError(f"Unsafe ZIP member: {member.filename}")
            archive.extractall(DATA_ROOT)
        private_volume.commit()

    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    before = count_jsonl(PREDICTIONS)
    print(f"Modal checkpoint before launch: {before:,}/141,000", flush=True)
    command = [
        "python",
        "-u",
        str(REMOTE_ROOT / "scripts/run_gemma_full.py"),
        "--repo-root",
        str(REMOTE_ROOT),
        "--data-root",
        str(DATA_ROOT),
        "--output-root",
        str(RUN_ROOT),
        "--repository-commit",
        REPOSITORY_COMMIT,
        "--batch-size",
        str(batch_size),
        "--max-new-tokens",
        "512",
        "--retry-max-new-tokens",
        "768",
        "--max-runtime-minutes",
        str(max_runtime_minutes),
    ]
    environment = os.environ.copy()
    environment["HF_HOME"] = "/root/.cache/huggingface"
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=environment,
    )
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True)
    return_code = process.wait()
    private_volume.commit()
    model_cache.commit()
    after = count_jsonl(PREDICTIONS)
    result = {
        "return_code": return_code,
        "checkpoint_before": before,
        "checkpoint_after": after,
        "generated_this_job": after - before,
        "complete": after == 141_000,
        "volume": VOLUME_NAME,
        "predictions_path": str(PREDICTIONS.relative_to(VOLUME_ROOT)),
    }
    print(json.dumps(result, indent=2), flush=True)
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, command)
    return result


@app.function(volumes={str(VOLUME_ROOT): private_volume})
def status() -> dict:
    private_volume.reload()
    state_path = RUN_ROOT / "session_state.json"
    metadata_path = RUN_ROOT / "run_metadata.json"
    result = {
        "predictions": count_jsonl(PREDICTIONS),
        "expected": 141_000,
        "complete": metadata_path.is_file(),
        "predictions_path": str(PREDICTIONS.relative_to(VOLUME_ROOT)),
    }
    if state_path.is_file():
        result["session_state"] = json.loads(state_path.read_text(encoding="utf-8"))
    return result


@app.local_entrypoint()
def main(
    action: str = "status",
    bundle: str = "",
    checkpoint: str = "",
    batch_size: int = 32,
    max_runtime_minutes: int = 600,
    replace: bool = False,
) -> None:
    """Upload private inputs, inspect status, or launch the paid GPU run."""
    if action == "upload":
        bundle_path = Path(bundle).expanduser().resolve()
        if not bundle_path.is_file() or bundle_path.name != "congolang-benchmark-v1.zip":
            raise ValueError("--bundle must point to congolang-benchmark-v1.zip")
        with ExitStack() as stack:
            files = [(bundle_path, "/input/congolang-benchmark-v1.zip")]
            if checkpoint:
                checkpoint_path = Path(checkpoint).expanduser().resolve()
                if not checkpoint_path.is_file():
                    raise ValueError("--checkpoint does not exist")
                if checkpoint_path.suffix.lower() == ".zip":
                    temporary = Path(stack.enter_context(tempfile.TemporaryDirectory()))
                    with zipfile.ZipFile(checkpoint_path) as archive:
                        members = [
                            name
                            for name in archive.namelist()
                            if Path(name).name == "predictions.jsonl"
                        ]
                        if len(members) != 1:
                            raise ValueError(
                                "Checkpoint ZIP must contain exactly one predictions.jsonl"
                            )
                        extracted = temporary / "predictions.jsonl"
                        extracted.write_bytes(archive.read(members[0]))
                        checkpoint_path = extracted
                elif checkpoint_path.name != "predictions.jsonl":
                    raise ValueError(
                        "--checkpoint must point to predictions.jsonl or its Drive ZIP"
                    )

                # Refuse a malformed or wrong-model checkpoint before it leaves this machine.
                count = 0
                with checkpoint_path.open(encoding="utf-8") as handle:
                    for line in handle:
                        if not line.strip():
                            continue
                        row = json.loads(line)
                        if row.get("model_id") != "google/gemma-4-12B-it":
                            raise ValueError("Checkpoint contains a different model")
                        count += 1
                if not count:
                    raise ValueError("Checkpoint is empty")
                print(f"Validated {count:,} local Gemma predictions.")
                files.append(
                    (checkpoint_path, "/runs/gemma4-12b-it-full-v1/predictions.jsonl")
                )
            with private_volume.batch_upload(force=replace) as upload:
                for local_path, remote_path in files:
                    upload.put_file(local_path, remote_path)
        print(f"Uploaded {len(files)} private file(s) to Modal volume {VOLUME_NAME}.")
    elif action == "run":
        if not 1 <= batch_size <= 128:
            raise ValueError("--batch-size must be between 1 and 128")
        if not 1 <= max_runtime_minutes <= 600:
            raise ValueError("--max-runtime-minutes must be between 1 and 600")
        print(run_gemma.remote(batch_size, max_runtime_minutes))
    elif action == "status":
        print(json.dumps(status.remote(), indent=2))
    else:
        raise ValueError("--action must be upload, run, or status")
