"""Normalize the complete available Havu--French eBible alignment."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/havu-hav/data/raw/hav-fr-v4408-v93.csv"
OUT = ROOT / "language_resources/havu-hav/data/processed"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    rows, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = clean(row["verse_key"])
            havu, french = clean(row["hav"]), clean(row["fr"])
            if not key or not havu or not french or (havu, french) in seen:
                continue
            seen.add((havu, french))
            rid = hashlib.sha256(f"hav-fr\0{havu}\0{french}".encode()).hexdigest()[:16]
            rows.append({
                "language": "Havu/Kihavu", "iso_code": "hav",
                "variety": "Havu (DRC)", "region": "South Kivu",
                "source": "Nouveau Testament Havu / French Louis Segond 1910",
                "source_url": "https://ebible.org/find/details.php?id=hav",
                "retrieved_at": "2026-08-22", "record_id": rid,
                "reference": key, "source_text": french,
                "target_language": "Havu/Kihavu", "target_text": havu,
                "unit_type": "verse", "domain": "religious",
                "licence": "CC BY-SA 4.0", "review_status": "verified_source",
                "quality_flags": "",
                "notes": "Havu copyright © 2025 The Seed Company; aligned with public-domain French Segond 1910.",
            })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "havu-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "havu-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Havu candidates")


if __name__ == "__main__":
    main()
