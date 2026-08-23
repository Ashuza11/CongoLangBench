"""Normalize and deduplicate the complete MT560 English--Songe dataset."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/songe-sop/data/raw/english-songe-train.parquet"
OUT = ROOT / "language_resources/songe-sop/data/processed"


def clean(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFC", text).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    frame = pd.read_parquet(RAW, columns=["eng", "sop"])
    rows, seen = [], set()
    for number, record in enumerate(frame.to_dict("records"), start=1):
        english, songe = clean(record["eng"]), clean(record["sop"])
        if not english or not songe or (english, songe) in seen:
            continue
        seen.add((english, songe))
        rid = hashlib.sha256(f"sop-en\0{english}\0{songe}".encode()).hexdigest()[:16]
        rows.append({
            "language": "Songe", "iso_code": "sop", "variety": "Songe / Kisonge",
            "region": "Kasai--Lomami transition zone, DRC",
            "source": "MT560 English--Songe",
            "source_url": "https://huggingface.co/datasets/michsethowusu/english-songe_sentence-pairs_mt560",
            "retrieved_at": "2026-08-23", "record_id": rid,
            "reference": f"train:{number}", "source_text": english,
            "target_language": "Songe", "target_text": songe,
            "unit_type": "sentence", "domain": "mixed", "licence": "CC BY 4.0",
            "review_status": "verified_source", "quality_flags": "mt560_mixed_provenance",
            "notes": "Dataset accepted as supplied; cite the wrapper dataset and original OPUS MT560 sources.",
        })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "songe-english_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "songe-english_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Songe candidates")


if __name__ == "__main__":
    main()
