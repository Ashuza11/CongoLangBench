"""Normalize locally available restricted Mongo--French alignments."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/mongo-lol/data/raw"
OUT = ROOT / "language_resources/mongo-lol/data/processed"
EDITIONS = {
    1495: "BONKANDA WA NZAKOMBA W’AEYOKO",
    2917: "BONKANDA WA NZAKOMBA",
}


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    rows, seen = [], set()
    for version_id, edition in EDITIONS.items():
        path = RAW / f"lol-fr-v{version_id}-v93.csv"
        if not path.exists():
            raise SystemExit(f"Missing restricted local alignment: {path}")
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for source_number, row in enumerate(csv.DictReader(handle), start=1):
                verse_key = clean(row["verse_key"])
                mongo, french = clean(row["lol"]), clean(row["fr"])
                pair = (mongo, french)
                if not verse_key or not mongo or not french or pair in seen:
                    continue
                seen.add(pair)
                record_id = hashlib.sha256(
                    f"lol-fr\0{mongo}\0{french}".encode()
                ).hexdigest()[:16]
                rows.append({
                    "language": "Mongo/Nkundo",
                    "iso_code": "lol",
                    "variety": f"Mongo/Nkundo (DRC; {edition})",
                    "region": "Northwestern DRC / Congo Basin",
                    "source": f"{edition} / French Louis Segond 1910",
                    "source_url": "https://huggingface.co/datasets/AfriSpeech/africa-corpus",
                    "retrieved_at": "2026-08-24",
                    "record_id": record_id,
                    "reference": verse_key,
                    "source_text": french,
                    "target_language": "Mongo/Nkundo",
                    "target_text": mongo,
                    "unit_type": "verse",
                    "domain": "religious",
                    "licence": "restricted / redistribution not authorized",
                    "review_status": "verified_source_restricted",
                    "quality_flags": "evaluation_only_not_publishable",
                    "notes": (
                        f"Mongo version {version_id} is marked copyrighted by "
                        "africa-bitext-builder 0.1.13; text remains Git-ignored."
                    ),
                    "source_version_id": version_id,
                    "source_row": source_number,
                })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    with (OUT / "mongo-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "mongo-french_candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} local restricted Mongo candidates")


if __name__ == "__main__":
    main()

