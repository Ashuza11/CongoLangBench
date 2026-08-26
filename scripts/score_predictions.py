"""Validate and score model predictions with BLEU and chrF++."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=Path)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    try:
        from sacrebleu.metrics import BLEU, CHRF
    except ImportError as exc:
        raise SystemExit(
            "sacrebleu is required. Install the pinned project requirements first."
        ) from exc

    jobs = load_jsonl(args.job)
    predictions = load_jsonl(args.predictions)
    expected_ids = [row["record_id"] for row in jobs]
    by_id = {}
    for row in predictions:
        record_id = row.get("record_id", "")
        prediction = row.get("prediction", "")
        if not record_id or not isinstance(prediction, str):
            raise ValueError("Every prediction needs string record_id and prediction fields")
        if record_id in by_id:
            raise ValueError(f"Duplicate prediction record_id: {record_id}")
        by_id[record_id] = prediction.strip()
    missing = [record_id for record_id in expected_ids if record_id not in by_id]
    extra = sorted(set(by_id) - set(expected_ids))
    if missing or extra:
        raise ValueError(f"Prediction coverage mismatch: {len(missing)} missing, {len(extra)} extra")

    hypotheses = [by_id[record_id] for record_id in expected_ids]
    references = [row["reference_text"] for row in jobs]
    empty = sum(not value for value in hypotheses)
    bleu_metric = BLEU()
    chrf_metric = CHRF(word_order=2)
    bleu = bleu_metric.corpus_score(hypotheses, [references])
    chrf = chrf_metric.corpus_score(hypotheses, [references])
    result = {
        "iso_code": jobs[0]["iso_code"],
        "benchmark_version": jobs[0]["benchmark_version"],
        "direction": jobs[0]["direction"],
        "prompt_version": jobs[0]["prompt_version"],
        "examples": len(jobs),
        "empty_predictions": empty,
        "bleu": bleu.score,
        "bleu_signature": str(bleu_metric.get_signature()),
        "chrf_plus_plus": chrf.score,
        "chrf_signature": str(chrf_metric.get_signature()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
