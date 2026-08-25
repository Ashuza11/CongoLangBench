"""Combine and normalize local restricted Logo--French alignments."""
from __future__ import annotations
import csv, hashlib, json, re, unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
RAW=ROOT/"language_resources/logo-log/data/raw"
OUT=ROOT/"language_resources/logo-log/data/processed"
EDITIONS={1834:"BÚKÙ TÀ TƗ́DHƗ́//RU YÌZO DHƗ ÀDHYA",2802:"Logo Gospel selections"}

def clean(value: str) -> str:
    return re.sub(r"\s+"," ",unicodedata.normalize("NFC",value or "").replace("\u00a0"," ")).strip()

def main() -> None:
    rows,seen=[],set()
    for version_id,edition in EDITIONS.items():
        path=RAW/f"log-fr-v{version_id}-v93.csv"
        with path.open(encoding="utf-8-sig",newline="") as handle:
            for number,row in enumerate(csv.DictReader(handle),start=1):
                key,logo,french=clean(row["verse_key"]),clean(row["log"]),clean(row["fr"]); pair=(logo,french)
                if not key or not logo or not french or pair in seen: continue
                seen.add(pair); rid=hashlib.sha256(f"log-fr\0{logo}\0{french}".encode()).hexdigest()[:16]
                rows.append({"language":"Logo/Logoti","iso_code":"log","variety":f"Logo/Logoti (DRC/South Sudan; {edition})",
                    "region":"Northern DRC / Uele","source":f"{edition} / French Louis Segond 1910",
                    "source_url":"https://huggingface.co/datasets/AfriSpeech/africa-corpus","retrieved_at":"2026-08-25",
                    "record_id":rid,"reference":key,"source_text":french,"target_language":"Logo/Logoti","target_text":logo,
                    "unit_type":"verse","domain":"religious","licence":"restricted / redistribution not authorized",
                    "review_status":"verified_source_restricted","quality_flags":"evaluation_only_not_publishable",
                    "notes":f"Logo version {version_id} is marked copyrighted by africa-bitext-builder 0.1.13; text remains Git-ignored.",
                    "source_version_id":version_id,"source_row":number})
    OUT.mkdir(parents=True,exist_ok=True); fields=list(rows[0]) if rows else []
    with (OUT/"logo-french_candidates.jsonl").open("w",encoding="utf-8") as h:
        for row in rows: h.write(json.dumps(row,ensure_ascii=False)+"\n")
    with (OUT/"logo-french_candidates.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields,lineterminator="\n"); w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows):,} local restricted Logo candidates")

if __name__=="__main__": main()
