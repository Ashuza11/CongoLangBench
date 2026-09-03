"""Validate and score a completed private full-model run without exporting text."""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from run_gemma_full import load_tracks, read_jsonl


def key(row: dict) -> tuple[str, str, str]:
    return row["iso_code"], row["direction"], row["record_id"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    from sacrebleu.metrics import BLEU, CHRF

    tracks = load_tracks(args.repo_root.resolve(), args.data_root.resolve())
    coverage_path = args.run_root / "coverage.json"
    if coverage_path.exists():
        coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
        supported = {row["iso_code"] for row in coverage if row["supported"]}
    else:
        supported = {track["iso_code"] for track in tracks}

    expected = {}
    track_metadata = {}
    for track in tracks:
        if track["iso_code"] not in supported:
            continue
        track_metadata[track["iso_code"]] = track
        with (args.data_root / track["benchmark_csv"]).open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            expected[(track["iso_code"], "reference_to_congolese", row["record_id"])] = row[
                "target_text"
            ]
            expected[(track["iso_code"], "congolese_to_reference", row["record_id"])] = row[
                "source_text"
            ]

    predictions = read_jsonl(args.run_root / "predictions.jsonl")
    metadata_path = args.run_root / "run_metadata.json"
    if not metadata_path.is_file():
        raise ValueError("run_metadata.json is absent: the production run is not complete")
    run_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    for field in ("model_id", "model_revision", "benchmark_version", "prompt_version"):
        values = {row.get(field) for row in predictions}
        if values != {run_metadata.get(field)}:
            raise ValueError(f"Mixed or unexpected {field}: {values}")
    by_key = {}
    for row in predictions:
        row_key = key(row)
        if row_key in by_key:
            raise ValueError(f"Duplicate prediction: {row_key}")
        by_key[row_key] = row
    missing = set(expected) - set(by_key)
    extra = set(by_key) - set(expected)
    if missing or extra:
        raise ValueError(
            f"Prediction coverage mismatch: {len(missing):,} missing, {len(extra):,} extra"
        )

    grouped = defaultdict(list)
    for row_key in expected:
        grouped[row_key[:2]].append(row_key)
    bleu = BLEU()
    chrf = CHRF(word_order=2)
    score_rows = []
    for (iso_code, direction), keys in sorted(grouped.items()):
        hypotheses = [by_key[row_key]["prediction"].strip() for row_key in keys]
        references = [expected[row_key] for row_key in keys]
        track = track_metadata[iso_code]
        score_rows.append(
            {
                "model_id": predictions[0]["model_id"],
                "language": track["language"],
                "iso_code": iso_code,
                "track": track["track"],
                "region_group": track["region_group"],
                "reference_language": track["reference_language"],
                "direction": direction,
                "examples": len(keys),
                "empty_predictions": sum(not text for text in hypotheses),
                "truncated_predictions": sum(
                    by_key[row_key].get("finish_reason") == "length" for row_key in keys
                ),
                "bleu": bleu.corpus_score(hypotheses, [references]).score,
                "chrf_plus_plus": chrf.corpus_score(hypotheses, [references]).score,
            }
        )

    args.output_root.mkdir(parents=True, exist_ok=True)
    scores_path = args.output_root / "scores.csv"
    with scores_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(score_rows[0]))
        writer.writeheader()
        writer.writerows(score_rows)
    validation = {
        "model_id": predictions[0]["model_id"],
        "supported_language_tracks": len(supported),
        "language_direction_groups": len(score_rows),
        "predictions": len(predictions),
        "expected_predictions": len(expected),
        "duplicates": 0,
        "missing": 0,
        "extra": 0,
        "empty_predictions": sum(row["empty_predictions"] for row in score_rows),
        "remaining_truncations": sum(row["truncated_predictions"] for row in score_rows),
        "bleu_signature": str(bleu.get_signature()),
        "chrf_plus_plus_signature": str(chrf.get_signature()),
    }
    (args.output_root / "validation.json").write_text(
        json.dumps(validation, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
