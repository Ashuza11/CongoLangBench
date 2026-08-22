"""Normalize and deduplicate all CLEAR Global French--Nande kits."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/nande-nnb/data/raw"
OUT = ROOT / "language_resources/nande-nnb/data/processed"
KITS = ("kit5k", "kit10k")
SOURCE_URL = "https://huggingface.co/datasets/CLEAR-Global/Gamayun-kits"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    rows, seen = [], set()
    for kit in KITS:
        path = RAW / f"nnb-fra-{kit}.tsv"
        with path.open(encoding="utf-8", newline="") as handle:
            for number, row in enumerate(csv.DictReader(handle, delimiter="\t"), start=2):
                french, nande = clean(row["fra"]), clean(row["nnb"])
                if not french or not nande or (french, nande) in seen:
                    continue
                seen.add((french, nande))
                rid = hashlib.sha256(f"nnb-fra\0{french}\0{nande}".encode()).hexdigest()[:16]
                rows.append({
                    "language": "Nande/Kinande",
                    "iso_code": "nnb",
                    "variety": "Nande (DRC)",
                    "region": "North Kivu",
                    "source": f"CLEAR Global Gamayun {kit}",
                    "source_url": SOURCE_URL,
                    "retrieved_at": "2026-08-22",
                    "record_id": rid,
                    "reference": f"{kit}:{number}",
                    "source_text": french,
                    "target_language": "Nande/Kinande",
                    "target_text": nande,
                    "unit_type": "sentence",
                    "domain": "general",
                    "licence": "CC BY 4.0",
                    "review_status": "verified_source",
                    "quality_flags": "",
                    "notes": "CLEAR Global source accepted as supplied; attribution required.",
                })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "nande-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "nande-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Nande candidates")


if __name__ == "__main__":
    main()
