"""Prepare SMOL Kituba sentence and document translations.

The GATITOS lexicon is intentionally not mixed into sentence bitext.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/kituba-ktu/data/raw"
OUT = ROOT / "language_resources/kituba-ktu/data/processed"
SOURCE_URL = "https://huggingface.co/datasets/google/smol"
QUALITY_FLAG = "smol_ktu_known_quality_warning"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "")
    return re.sub(r"\s+", " ", value.replace("\u00a0", " ")).strip()


def make_row(source: str, reference: str, english: str, kituba: str, seen: set[tuple[str, str]]):
    english, kituba = clean(english), clean(kituba)
    if not english or not kituba or (english, kituba) in seen:
        return None
    seen.add((english, kituba))
    rid = hashlib.sha256(f"ktu-en\0{english}\0{kituba}".encode()).hexdigest()[:16]
    return {
        "language": "Kikongo ya Leta",
        "iso_code": "ktu",
        "variety": "Kituba (DRC)",
        "region": "Western DRC",
        "source": source,
        "source_url": SOURCE_URL,
        "retrieved_at": "2026-08-21",
        "record_id": rid,
        "reference": reference,
        "source_text": english,
        "target_language": "Kikongo ya Leta",
        "target_text": kituba,
        "unit_type": "sentence",
        "domain": "general",
        "licence": "CC BY 4.0",
        "review_status": "verified_source",
        "quality_flags": QUALITY_FLAG,
        "notes": "Authentic SMOL source accepted as supplied; retain known Kituba quality warning.",
    }


def main() -> None:
    rows, seen = [], set()
    with (RAW / "ktu-en-smolsent.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            item = json.loads(line)
            row = make_row("Google SMOL SmolSent en_ktu", f"smolsent:{item['id']}", item["src"], item["trg"], seen)
            if row:
                rows.append(row)
    with (RAW / "ktu-en-smoldoc.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            item = json.loads(line)
            for index, (english, kituba) in enumerate(zip(item["srcs"], item["trgs"])):
                row = make_row("Google SMOL SmolDoc en_ktu", f"smoldoc:{item['id']}:{index}", english, kituba, seen)
                if row:
                    rows.append(row)
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "kituba-english_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "kituba-english_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Kituba sentence candidates")


if __name__ == "__main__":
    main()
