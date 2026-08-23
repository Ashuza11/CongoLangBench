"""Normalize the African Languages Lab English--Kikongo split."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install pandas and pyarrow before running this script") from exc


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/kikongo-kon/data/raw/english-kikongo-train.parquet"
OUT = ROOT / "language_resources/kikongo-kon/data/processed"


def clean(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFC", text.replace("\u00a0", " "))
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    if not RAW.exists():
        raise SystemExit(f"Missing {RAW}; download the accepted dataset file first")
    frame = pd.read_parquet(RAW)
    required = {"english", "kikongo"}
    missing = required - set(frame.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")

    rows, seen = [], set()
    for number, record in enumerate(frame.to_dict("records"), start=1):
        english = clean(record.get("english"))
        kikongo = clean(record.get("kikongo"))
        if not english or not kikongo or (english, kikongo) in seen:
            continue
        seen.add((english, kikongo))
        score = record.get("translation_quality_score")
        score = None if pd.isna(score) else int(score)
        record_id = hashlib.sha256(
            f"kon-en\0{english}\0{kikongo}".encode()
        ).hexdigest()[:16]
        rows.append({
            "language": "Kikongo/Koongo",
            "iso_code": "kon",
            "variety": "Kikongo (source label; exact regional variety unspecified)",
            "region": "Western DRC / Kongo language area",
            "source": "African Languages Lab multi-open",
            "source_url": "https://huggingface.co/datasets/African-Languages-Lab/multi-open",
            "retrieved_at": "2026-08-23",
            "record_id": record_id,
            "reference": f"train:{number}",
            "source_text": english,
            "target_language": "Kikongo/Koongo",
            "target_text": kikongo,
            "unit_type": "sentence",
            "domain": "mixed",
            "licence": "other (dataset terms)",
            "review_status": "verified_source_variety_unspecified",
            "translation_quality_score": score,
            "quality_flags": (
                "automatic_gemma_score_not_human_gold;exact_kikongo_variety_unspecified"
                if score is not None else
                "quality_score_missing;exact_kikongo_variety_unspecified"
            ),
            "notes": (
                "Accepted source dataset; Kikongo is a DRC language, but the source "
                "does not identify each row as a specifically DRC Kikongo variety."
            ),
        })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    with (OUT / "kikongo-english_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "kikongo-english_candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Kikongo candidates")


if __name__ == "__main__":
    main()

