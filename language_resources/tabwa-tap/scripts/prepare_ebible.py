"""Normalize the complete available Tabwa--French eBible alignment."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/tabwa-tap/data/raw/tap-fr-v4387-v93.csv"
OUT = ROOT / "language_resources/tabwa-tap/data/processed"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    rows, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = clean(row["verse_key"])
            tabwa, french = clean(row["tap"]), clean(row["fr"])
            if not key or not tabwa or not french or (tabwa, french) in seen:
                continue
            seen.add((tabwa, french))
            rid = hashlib.sha256(f"tap-fr\0{tabwa}\0{french}".encode()).hexdigest()[:16]
            rows.append({
                "language": "Tabwa/Kitabwa", "iso_code": "tap",
                "variety": "Taabwa (DRC)", "region": "Southeastern DRC",
                "source": "Kitaabua New Testament / French Louis Segond 1910",
                "source_url": "https://ebible.org/Scriptures/details.php?id=tap",
                "retrieved_at": "2026-08-22", "record_id": rid,
                "reference": key, "source_text": french,
                "target_language": "Tabwa/Kitabwa", "target_text": tabwa,
                "unit_type": "verse", "domain": "religious",
                "licence": "CC BY-SA 4.0", "review_status": "verified_source",
                "quality_flags": "",
                "notes": "Tabwa copyright © 2023 The Word for the World International; aligned with public-domain French Segond 1910.",
            })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "tabwa-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "tabwa-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Tabwa candidates")


if __name__ == "__main__":
    main()
