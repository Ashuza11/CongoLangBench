"""Normalize the local restricted Tembo--French package alignment."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/tembo-tbt/data/raw/tbt-fr-v3997-v93.csv"
OUT = ROOT / "language_resources/tembo-tbt/data/processed"


def clean(value: str) -> str:
    return re.sub(
        r"\s+", " ", unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    ).strip()


def main() -> None:
    rows, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for number, raw in enumerate(csv.DictReader(handle), 1):
            reference = clean(raw["verse_key"])
            target, french = clean(raw["tbt"]), clean(raw["fr"])
            pair = (target, french)
            if not reference or not target or not french or pair in seen:
                continue
            seen.add(pair)
            record_id = hashlib.sha256(f"tbt-fr\0{target}\0{french}".encode()).hexdigest()[:16]
            rows.append({
                "language": "Tembo/Kitembo", "iso_code": "tbt",
                "variety": "Tembo (DRC)", "region": "North/South Kivu transition",
                "source": "Echilaano Chiyayaya v3997 / French Louis Segond 1910",
                "source_url": "https://huggingface.co/datasets/AfriSpeech/africa-corpus",
                "retrieved_at": "2026-08-26", "record_id": record_id,
                "reference": reference, "source_text": french,
                "target_language": "Tembo/Kitembo", "target_text": target,
                "unit_type": "verse", "domain": "religious",
                "licence": "restricted / redistribution not authorized",
                "review_status": "verified_source_restricted",
                "quality_flags": "evaluation_only_not_publishable",
                "notes": "Authentic package edition retained as supplied; raw and derived text remain Git-ignored.",
                "source_version_id": 3997, "source_row": number,
            })
    if len(rows) < 1500:
        raise RuntimeError(f"Only {len(rows):,} usable pairs; 1,500 required")
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "tembo-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    with (OUT / "tembo-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows):,} local restricted Tembo candidates")


if __name__ == "__main__":
    main()
