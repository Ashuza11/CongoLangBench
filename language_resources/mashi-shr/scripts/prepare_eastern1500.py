"""Create the deterministic 1,500-pair Eastern Mashi benchmark track."""

from __future__ import annotations

import csv
import hashlib
import json
import random
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/mashi-shr/data/raw/shr-fr-v3953-v93.csv"
OUT = ROOT / "language_resources/mashi-shr/data/processed"
SAMPLE_SIZE = 1_500
SEED = 42


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    candidates, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = clean(row["verse_key"])
            mashi, french = clean(row["shr"]), clean(row["fr"])
            if not key or not mashi or not french or (mashi, french) in seen:
                continue
            seen.add((mashi, french))
            candidates.append((key, mashi, french))

    if len(candidates) < SAMPLE_SIZE:
        raise SystemExit(f"Only {len(candidates)} usable pairs; need {SAMPLE_SIZE}")
    selected = random.Random(SEED).sample(candidates, SAMPLE_SIZE)
    selected.sort(key=lambda item: item[0])

    rows = []
    for key, mashi, french in selected:
        rid = hashlib.sha256(f"shr-fr\0{mashi}\0{french}".encode()).hexdigest()[:16]
        rows.append({
            "language": "Mashi/Shi", "iso_code": "shr",
            "variety": "Mashi (DRC)", "region": "South Kivu",
            "source": "BIBLIYA NTAGATIFU OMU MASHI / French Louis Segond 1910",
            "source_url": "https://ebible.org/find/details.php?id=shr",
            "retrieved_at": "2026-08-22", "record_id": rid,
            "reference": key, "source_text": french,
            "target_language": "Mashi/Shi", "target_text": mashi,
            "unit_type": "verse", "domain": "religious",
            "licence": "CC BY 4.0", "review_status": "verified_source",
            "quality_flags": "",
            "notes": "Authentic open Mashi source retained as supplied; deterministic Eastern-track sample.",
        })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "mashi-french_eastern1500.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "mashi-french_eastern1500.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} pairs from {len(candidates):,} unique candidates")


if __name__ == "__main__":
    main()
