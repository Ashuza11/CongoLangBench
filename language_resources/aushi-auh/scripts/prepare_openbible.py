"""Normalize the complete available Aushi--French verse alignment."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/aushi-auh/data/raw/auh-fr-v4447-v93.csv"
OUT = ROOT / "language_resources/aushi-auh/data/processed"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    rows, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = clean(row["verse_key"])
            aushi, french = clean(row["auh"]), clean(row["fr"])
            if not key or not aushi or not french or (aushi, french) in seen:
                continue
            seen.add((aushi, french))
            rid = hashlib.sha256(f"auh-fr\0{aushi}\0{french}".encode()).hexdigest()[:16]
            rows.append({
                "language": "Aushi", "iso_code": "auh",
                "variety": "Aushi (Zambia source; cross-border DRC candidate)",
                "region": "Southeastern DRC / Zambia border zone",
                "source": "Aushi Bible Translation Project / French Louis Segond 1910",
                "source_url": "https://preview.open.bible/bibles/aushi-bible-translation-project",
                "retrieved_at": "2026-08-22", "record_id": rid,
                "reference": key, "source_text": french,
                "target_language": "Aushi", "target_text": aushi,
                "unit_type": "verse", "domain": "religious",
                "licence": "CC BY-SA 4.0", "review_status": "verified_source",
                "quality_flags": "cross_border_variety;below_1500_target",
                "notes": "Aushi edition provided by The Word for the World International for Zambia; aligned with public-domain French Segond 1910.",
            })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "aushi-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "aushi-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Aushi candidates")


if __name__ == "__main__":
    main()
