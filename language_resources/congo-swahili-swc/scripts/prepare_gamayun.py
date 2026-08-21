"""Prepare CLEAR Global Congo Swahili TSV kits as review-ready candidates.

Raw TSV files are never modified. The output is deduplicated across kits and
uses the repository-wide bitext metadata fields.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = ROOT / "language_resources/congo-swahili-swc/data/raw"
OUT_DIR = ROOT / "language_resources/congo-swahili-swc/data/processed"
SOURCE_URL = "https://huggingface.co/datasets/CLEAR-Global/Gamayun-kits"
LICENCE = "CC BY 4.0"
RETRIEVED_AT = "2026-08-21"


def clean_text(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "")
    return re.sub(r"\s+", " ", value.replace("\u00a0", " ")).strip()


def record_id(french: str, swc: str) -> str:
    payload = f"swc-fra\0{french}\0{swc}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def read_rows():
    seen = set()
    rows = []
    for path in sorted(RAW_DIR.glob("swc-fra-*.tsv")):
        kit = path.stem.removeprefix("swc-fra-")
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            required = {"fra", "swc", "swc_clean"}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"{path}: missing columns {sorted(missing)}")
            for row_number, row in enumerate(reader, start=2):
                french = clean_text(row["fra"])
                swc = clean_text(row["swc"])
                swc_clean = clean_text(row["swc_clean"])
                if not french or not swc:
                    continue
                key = (french, swc)
                if key in seen:
                    continue
                seen.add(key)
                flags = []
                if swc != swc_clean:
                    flags.append("clean_variant_diff")
                rows.append(
                    {
                        "language": "Congo Swahili",
                        "iso_code": "swc",
                        "variety": "DRC Congo Swahili",
                        "region": "Eastern DRC",
                        "source": f"CLEAR Global Gamayun {kit}",
                        "source_url": SOURCE_URL,
                        "retrieved_at": RETRIEVED_AT,
                        "record_id": record_id(french, swc),
                        "reference": f"{kit}:{row_number}",
                        "source_text": french,
                        "target_language": "Congo Swahili",
                        "target_text": swc_clean,
                        "target_text_raw": swc,
                        "unit_type": "sentence",
                        "domain": "general",
                        "licence": LICENCE,
                        "review_status": "needs_review",
                        "quality_flags": ";".join(flags),
                        "notes": "Do not use as a final benchmark row before native-speaker review.",
                    }
                )
    return rows


def main():
    rows = read_rows()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    jsonl_path = OUT_DIR / "congo-swahili-french_candidates.jsonl"
    csv_path = OUT_DIR / "congo-swahili-french_candidates.csv"
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique candidates")
    print(jsonl_path)
    print(csv_path)


if __name__ == "__main__":
    main()
