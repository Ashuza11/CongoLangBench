"""Create a local model-evaluation job from a frozen language benchmark."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "benchmark_freeze.csv"
PROMPT_PATH = ROOT / "evaluations" / "prompts" / "translation_v1.txt"
JOBS = ROOT / "evaluations" / "jobs"
DIRECTIONS = ("reference_to_congolese", "congolese_to_reference")


def manifest_row(iso_code: str) -> dict[str, str]:
    with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        matches = [row for row in csv.DictReader(handle) if row["iso_code"] == iso_code]
    if len(matches) != 1:
        raise ValueError(f"Expected one frozen track for {iso_code!r}; found {len(matches)}")
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("iso_code")
    parser.add_argument("direction", choices=DIRECTIONS)
    parser.add_argument("--limit", type=int, default=0, help="Smoke-test limit; 0 uses all frozen rows")
    args = parser.parse_args()

    track = manifest_row(args.iso_code.lower())
    benchmark = ROOT / track["benchmark_csv"]
    with benchmark.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if args.limit:
        if args.limit < 1:
            raise ValueError("--limit must be positive")
        rows = rows[: args.limit]
    template = PROMPT_PATH.read_text(encoding="utf-8").strip()
    language = track["language"]
    reference_language = track["reference_language"]

    JOBS.mkdir(parents=True, exist_ok=True)
    run_label = f"smoke-{args.limit}" if args.limit else "full"
    output = JOBS / (
        f"{args.iso_code}-{args.direction}-{track['benchmark_version']}-{run_label}.jsonl"
    )
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            if args.direction == "reference_to_congolese":
                input_text, expected = row["source_text"], row["target_text"]
                source_language, target_language = reference_language, language
            else:
                input_text, expected = row["target_text"], row["source_text"]
                source_language, target_language = language, reference_language
            record = {
                "record_id": row["record_id"],
                "iso_code": args.iso_code,
                "benchmark_version": track["benchmark_version"],
                "benchmark_sha256": track["benchmark_sha256"],
                "job_kind": "smoke_test" if args.limit else "final_full_set",
                "job_record_count": len(rows),
                "direction": args.direction,
                "source_language": source_language,
                "target_language": target_language,
                "input_text": input_text,
                "reference_text": expected,
                "prompt_version": "translation_v1",
                "prompt": template.format(
                    source_language=source_language,
                    target_language=target_language,
                    input_text=input_text,
                ),
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    label = f"{args.limit}-record smoke test" if args.limit else "final full-set job"
    print(f"Wrote {len(rows):,} records ({label}) to {output}")


if __name__ == "__main__":
    main()
