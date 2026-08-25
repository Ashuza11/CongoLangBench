"""Normalize the local restricted Kele/Lokele--French alignment."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/kele-khy/data/raw/khy-fr-v1496-v93.csv"
OUT = ROOT / "language_resources/kele-khy/data/processed"


def clean(value: str) -> str:
    return re.sub(
        r"\s+", " ", unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    ).strip()


def main() -> None:
    rows = []
    seen = set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for source_row, raw in enumerate(csv.DictReader(handle), 1):
            reference = clean(raw["verse_key"])
            target = clean(raw["khy"])
            french = clean(raw["fr"])
            pair = (french, target)
            if not reference or not target or not french or pair in seen:
                continue
            seen.add(pair)
            record_id = hashlib.sha256(
                f"khy-fr\0{french}\0{target}".encode()
            ).hexdigest()[:16]
            rows.append(
                {
                    "language": "Kele/Lokele",
                    "iso_code": "khy",
                    "variety": "Kele/Lokele (DRC)",
                    "region": "Tshopo / Kisangani",
                    "source": "Le Nouveau Testament in Kele (Lokele) 1958 / French Louis Segond 1910",
                    "source_url": "https://huggingface.co/datasets/AfriSpeech/africa-corpus",
                    "retrieved_at": "2026-08-25",
                    "record_id": record_id,
                    "reference": reference,
                    "source_text": french,
                    "target_language": "Kele/Lokele",
                    "target_text": target,
                    "unit_type": "verse",
                    "domain": "religious",
                    "licence": "restricted / redistribution not authorized",
                    "review_status": "verified_source_restricted",
                    "quality_flags": "evaluation_only_not_publishable",
                    "notes": "Version 1496 is marked copyrighted by africa-bitext-builder 0.1.13; text remains Git-ignored.",
                    "source_version_id": 1496,
                    "source_row": source_row,
                }
            )

    if not rows:
        raise RuntimeError("No Kele/Lokele pairs were produced")
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "kele-french_candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "kele-french_candidates.jsonl").open(
        "w", encoding="utf-8"
    ) as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows):,} local restricted Kele/Lokele candidates")


if __name__ == "__main__":
    main()
