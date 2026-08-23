"""Normalize the complete public-domain Yaka--French package alignment."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/yaka-yaf/data/raw/yaf-fr-v3951-v93.csv"
OUT = ROOT / "language_resources/yaka-yaf/data/processed"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    rows, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = clean(row["verse_key"])
            yaka, french = clean(row["yaf"]), clean(row["fr"])
            if not key or not yaka or not french or (yaka, french) in seen:
                continue
            seen.add((yaka, french))
            rid = hashlib.sha256(f"yaf-fr\0{yaka}\0{french}".encode()).hexdigest()[:16]
            rows.append({
                "language": "Yaka", "iso_code": "yaf",
                "variety": "Yaka (DRC--Angola source)",
                "region": "Western DRC / Kwango",
                "source": "Yaka NT / French Louis Segond 1910",
                "source_url": "https://huggingface.co/datasets/AfriSpeech/africa-corpus",
                "retrieved_at": "2026-08-23", "record_id": rid,
                "reference": key, "source_text": french,
                "target_language": "Yaka", "target_text": yaka,
                "unit_type": "verse", "domain": "religious", "licence": "Public Domain",
                "review_status": "verified_source", "quality_flags": "cross_border_variety",
                "notes": "Yaka version 3951 is marked public domain and associated with CD and AO by africa-bitext-builder 0.1.13; French version 93 is public domain.",
            })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "yaka-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "yaka-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Yaka candidates")


if __name__ == "__main__":
    main()
