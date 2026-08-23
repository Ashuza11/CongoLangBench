"""Normalize the complete public-domain Yansi--French package alignment."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/yansi-yns/data/raw/yns-fr-v3929-v93.csv"
OUT = ROOT / "language_resources/yansi-yns/data/processed"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    rows, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = clean(row["verse_key"])
            yansi, french = clean(row["yns"]), clean(row["fr"])
            if not key or not yansi or not french or (yansi, french) in seen:
                continue
            seen.add((yansi, french))
            rid = hashlib.sha256(f"yns-fr\0{yansi}\0{french}".encode()).hexdigest()[:16]
            rows.append({
                "language": "Yansi", "iso_code": "yns", "variety": "Yansi / Yanzi (DRC)",
                "region": "Western DRC / Kwilu--Mai-Ndombe",
                "source": "Bible Iyansi / French Louis Segond 1910",
                "source_url": "https://huggingface.co/datasets/AfriSpeech/africa-corpus",
                "retrieved_at": "2026-08-23", "record_id": rid,
                "reference": key, "source_text": french,
                "target_language": "Yansi", "target_text": yansi,
                "unit_type": "verse", "domain": "religious", "licence": "Public Domain",
                "review_status": "verified_source", "quality_flags": "",
                "notes": "Yansi version 3929 and French version 93 are marked public domain by africa-bitext-builder 0.1.13.",
            })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "yansi-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "yansi-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Yansi candidates")


if __name__ == "__main__":
    main()
