"""Normalize and deduplicate the CLEAR Global Lingala–French kit."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/lingala-lin/data/raw/lin-fra-kit5k.tsv"
OUT = ROOT / "language_resources/lingala-lin/data/processed"
SOURCE_URL = "https://huggingface.co/datasets/CLEAR-Global/Gamayun-kits"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "")
    return re.sub(r"\s+", " ", value.replace("\u00a0", " ")).strip()


def main() -> None:
    rows, seen = [], set()
    with RAW.open(encoding="utf-8", newline="") as handle:
        for number, row in enumerate(csv.DictReader(handle, delimiter="\t"), start=2):
            french, lingala = clean(row["fra"]), clean(row["lin"])
            if not french or not lingala or (french, lingala) in seen:
                continue
            seen.add((french, lingala))
            rid = hashlib.sha256(f"lin-fra\0{french}\0{lingala}".encode()).hexdigest()[:16]
            rows.append({
                "language": "Lingala",
                "iso_code": "lin",
                "variety": "DRC Lingala",
                "region": "DRC-wide",
                "source": "CLEAR Global Gamayun kit5k",
                "source_url": SOURCE_URL,
                "retrieved_at": "2026-08-21",
                "record_id": rid,
                "reference": f"kit5k:{number}",
                "source_text": french,
                "target_language": "Lingala",
                "target_text": lingala,
                "unit_type": "sentence",
                "domain": "general",
                "licence": "CC BY 4.0",
                "review_status": "verified_source",
                "quality_flags": "",
                "notes": "CLEAR Global source accepted as supplied; source provenance and licence documented.",
            })
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "lingala-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "lingala-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Lingala candidates")


if __name__ == "__main__":
    main()
