"""Create the deterministic internal Nande--French curation set."""

from __future__ import annotations

import csv
import hashlib
import json
import random
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/nande-nnb/data/raw/nnb-fr-v1833-v93.csv"
OUT = ROOT / "language_resources/nande-nnb/data/processed"
SAMPLE_SIZE = 1_500
SEED = 42


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def main() -> None:
    candidates, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            nande, french = clean(row["nnb"]), clean(row["fr"])
            key = clean(row["verse_key"])
            if not key or not nande or not french or (nande, french) in seen:
                continue
            seen.add((nande, french))
            candidates.append((key, nande, french))

    if len(candidates) < SAMPLE_SIZE:
        raise SystemExit(f"Only {len(candidates)} usable pairs; need {SAMPLE_SIZE}")
    selected = random.Random(SEED).sample(candidates, SAMPLE_SIZE)
    selected.sort(key=lambda item: item[0])

    rows = []
    for key, nande, french in selected:
        record_id = hashlib.sha256(f"nnb-fr\0{nande}\0{french}".encode()).hexdigest()[:16]
        rows.append({
            "language": "Nande/Kinande", "iso_code": "nnb",
            "variety": "Kinandi (Ndandi), DRC", "region": "North Kivu",
            "source": "AfriSpeech Africa Corpus Builder, Nande v1833 / French LSG v93",
            "source_url": "https://huggingface.co/datasets/AfriSpeech/africa-corpus",
            "retrieved_at": "2026-08-22", "record_id": record_id,
            "reference": key, "source_text": french,
            "target_language": "Nande/Kinande", "target_text": nande,
            "unit_type": "verse", "domain": "religious",
            "licence": "other; source terms restrict redistribution",
            "review_status": "verified_source",
            "quality_flags": "restricted_redistribution",
            "notes": "Authentic source retained as supplied; internal research curation only pending redistribution permission.",
        })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "nande-french-curated.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "nande-french-curated.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} pairs from {len(candidates):,} unique candidates")


if __name__ == "__main__":
    main()
