"""Combine and normalize all open Ngombe--French package alignments."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/ngombe-ngc/data/raw"
OUT = ROOT / "language_resources/ngombe-ngc/data/processed"
EDITIONS = {
    4524: "Miwera",
    4525: "Bodjenga NT and OT",
    4527: "Bondjale",
}


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    rows, seen = [], set()
    for version_id, edition in EDITIONS.items():
        path = RAW / f"ngc-fr-v{version_id}-v93.csv"
        if not path.exists():
            raise SystemExit(f"Missing raw alignment: {path}")
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for source_number, row in enumerate(csv.DictReader(handle), start=1):
                verse_key = clean(row["verse_key"])
                ngombe, french = clean(row["ngc"]), clean(row["fr"])
                pair = (ngombe, french)
                if not verse_key or not ngombe or not french or pair in seen:
                    continue
                seen.add(pair)
                record_id = hashlib.sha256(
                    f"ngc-fr\0{ngombe}\0{french}".encode()
                ).hexdigest()[:16]
                rows.append({
                    "language": "Ngombe",
                    "iso_code": "ngc",
                    "variety": f"Ngombe (DRC source; {edition})",
                    "region": "Northwestern DRC / Congo Basin",
                    "source": f"{edition} / French Louis Segond 1910",
                    "source_url": "https://huggingface.co/datasets/AfriSpeech/africa-corpus",
                    "retrieved_at": "2026-08-24",
                    "record_id": record_id,
                    "reference": verse_key,
                    "source_text": french,
                    "target_language": "Ngombe",
                    "target_text": ngombe,
                    "unit_type": "verse",
                    "domain": "religious",
                    "licence": "Public Domain",
                    "review_status": "verified_source",
                    "quality_flags": "",
                    "notes": (
                        f"Ngombe version {version_id} and French version 93 are "
                        "marked public domain by africa-bitext-builder 0.1.13."
                    ),
                    "source_version_id": version_id,
                    "source_row": source_number,
                })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    with (OUT / "ngombe-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "ngombe-french_candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Ngombe candidates")


if __name__ == "__main__":
    main()

