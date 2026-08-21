"""Normalize the gated African Languages Lab English--Tshiluba split.

The file must be downloaded after accepting the dataset terms on Hugging Face
and authenticating the local environment. Automatic quality scores are retained
as metadata; they are not human annotations.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install pandas and pyarrow before running this script") from exc


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/ciluba-lua/data/raw/english-tshiluba-train.parquet"
OUT = ROOT / "language_resources/ciluba-lua/data/processed"


def clean(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFC", text.replace("\u00a0", " "))
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    if not RAW.exists():
        raise SystemExit(f"Missing {RAW}; download the gated file first")
    frame = pd.read_parquet(RAW)
    required = {"english", "tshiluba"}
    missing = required - set(frame.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")

    rows, seen = [], set()
    for number, record in enumerate(frame.to_dict("records"), start=1):
        english, tshiluba = clean(record.get("english")), clean(record.get("tshiluba"))
        if not english or not tshiluba or (english, tshiluba) in seen:
            continue
        seen.add((english, tshiluba))
        score = record.get("translation_quality_score")
        score = None if pd.isna(score) else int(score)
        rid = hashlib.sha256(f"lua-en\\0{english}\\0{tshiluba}".encode()).hexdigest()[:16]
        rows.append({
            "language": "Ciluba/Tshiluba",
            "iso_code": "lua",
            "variety": "Luba-Kasai (DRC)",
            "region": "Kasai",
            "source": "African Languages Lab multi-open",
            "source_url": "https://huggingface.co/datasets/African-Languages-Lab/multi-open",
            "retrieved_at": "2026-08-21",
            "record_id": rid,
            "reference": f"train:{number}",
            "source_text": english,
            "target_language": "Ciluba/Tshiluba",
            "target_text": tshiluba,
            "unit_type": "sentence",
            "domain": "mixed",
            "licence": "other (dataset terms)",
            "review_status": "verified_source",
            "translation_quality_score": score,
            "quality_flags": "automatic_gemma_score_not_human_gold" if score is not None else "quality_score_missing",
            "notes": "Gated source accepted under dataset terms; automatic quality score retained for analysis only.",
        })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    with (OUT / "ciluba-english_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "ciluba-english_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Ciluba candidates")


if __name__ == "__main__":
    main()
