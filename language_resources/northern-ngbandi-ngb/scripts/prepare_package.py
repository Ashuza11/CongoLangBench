"""Normalize the local restricted Northern Ngbandi--French alignment."""
from __future__ import annotations
import csv, hashlib, json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/northern-ngbandi-ngb/data/raw/ngb-fr-v2682-v93.csv"
OUT = ROOT / "language_resources/northern-ngbandi-ngb/data/processed"

def clean(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")).strip()

def main() -> None:
    rows, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for number, row in enumerate(csv.DictReader(handle), start=1):
            key, ngbandi, french = clean(row["verse_key"]), clean(row["ngb"]), clean(row["fr"])
            pair = (ngbandi, french)
            if not key or not ngbandi or not french or pair in seen: continue
            seen.add(pair)
            rid = hashlib.sha256(f"ngb-fr\0{ngbandi}\0{french}".encode()).hexdigest()[:16]
            rows.append({
                "language":"Northern Ngbandi", "iso_code":"ngb", "variety":"Northern Ngbandi (DRC/CAR source)",
                "region":"Northwestern DRC / Ubangi", "source":"Fana Ngbangɔ 1987 / French Louis Segond 1910",
                "source_url":"https://huggingface.co/datasets/AfriSpeech/africa-corpus", "retrieved_at":"2026-08-24",
                "record_id":rid, "reference":key, "source_text":french,
                "target_language":"Northern Ngbandi", "target_text":ngbandi,
                "unit_type":"verse", "domain":"religious", "licence":"restricted / redistribution not authorized",
                "review_status":"verified_source_restricted", "quality_flags":"evaluation_only_not_publishable",
                "notes":"Northern Ngbandi version 2682 is marked copyrighted by africa-bitext-builder 0.1.13; text remains Git-ignored.",
                "source_version_id":2682, "source_row":number,
            })
    OUT.mkdir(parents=True, exist_ok=True); fields=list(rows[0]) if rows else []
    with (OUT/"northern-ngbandi-french_candidates.jsonl").open("w",encoding="utf-8") as h:
        for row in rows: h.write(json.dumps(row,ensure_ascii=False)+"\n")
    with (OUT/"northern-ngbandi-french_candidates.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields,lineterminator="\n"); w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows):,} local restricted Northern Ngbandi candidates")

if __name__ == "__main__": main()
