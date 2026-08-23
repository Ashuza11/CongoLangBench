"""Normalize and deduplicate the complete MT560 English--Ruund dataset."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/ruund-rnd/data/raw/english-ruund-train.parquet"
OUT = ROOT / "language_resources/ruund-rnd/data/processed"


def clean(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFC", text).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    frame = pd.read_parquet(RAW, columns=["eng", "rnd"])
    rows, seen = [], set()
    for number, record in enumerate(frame.to_dict("records"), start=1):
        english, ruund = clean(record["eng"]), clean(record["rnd"])
        if not english or not ruund or (english, ruund) in seen:
            continue
        seen.add((english, ruund))
        rid = hashlib.sha256(f"rnd-en\0{english}\0{ruund}".encode()).hexdigest()[:16]
        rows.append({
            "language": "Ruund", "iso_code": "rnd", "variety": "Ruund / Uruund",
            "region": "Kasai--Lualaba transition zone, DRC",
            "source": "MT560 English--Ruund",
            "source_url": "https://huggingface.co/datasets/michsethowusu/english-ruund_sentence-pairs_mt560",
            "retrieved_at": "2026-08-23", "record_id": rid,
            "reference": f"train:{number}", "source_text": english,
            "target_language": "Ruund", "target_text": ruund,
            "unit_type": "sentence", "domain": "mixed", "licence": "CC BY 4.0",
            "review_status": "verified_source", "quality_flags": "mt560_mixed_provenance",
            "notes": "Dataset accepted as supplied; cite the wrapper dataset and original OPUS MT560 sources.",
        })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "ruund-english_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "ruund-english_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Ruund candidates")


if __name__ == "__main__":
    main()
