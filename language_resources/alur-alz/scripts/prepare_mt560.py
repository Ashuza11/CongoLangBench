"""Normalize and deduplicate the complete MT560 English--Alur dataset."""
from __future__ import annotations
import csv,hashlib,json,re,unicodedata
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];RAW=ROOT/"language_resources/alur-alz/data/raw/english-alur-train.parquet";OUT=ROOT/"language_resources/alur-alz/data/processed"
def clean(v:object)->str:return re.sub(r"\s+"," ",unicodedata.normalize("NFC","" if v is None else str(v)).replace("\u00a0"," ")).strip()
def main()->None:
 frame=pd.read_parquet(RAW,columns=["eng","alz"]);rows=[];seen=set()
 for n,r in enumerate(frame.to_dict("records"),1):
  source,target=clean(r["eng"]),clean(r["alz"]);pair=(source,target)
  if not source or not target or pair in seen:continue
  seen.add(pair);rid=hashlib.sha256(f"alz-en\0{source}\0{target}".encode()).hexdigest()[:16]
  rows.append({"language":"Alur/Dho-Alur","iso_code":"alz","variety":"Alur (dataset country label: DRC)","region":"Ituri / Mahagi","source":"MT560 English--Alur","source_url":"https://huggingface.co/datasets/michsethowusu/english-alur_sentence-pairs_mt560","retrieved_at":"2026-08-25","record_id":rid,"reference":f"train:{n}","source_text":source,"target_language":"Alur","target_text":target,"unit_type":"sentence","domain":"mixed","licence":"CC BY 4.0","review_status":"verified_source","quality_flags":"mt560_mixed_provenance","notes":"Dataset accepted as supplied; cite wrapper and original OPUS MT560 sources."})
 OUT.mkdir(parents=True,exist_ok=True);fields=list(rows[0]) if rows else []
 with (OUT/"alur-english_candidates.jsonl").open("w",encoding="utf-8") as h:
  for row in rows:h.write(json.dumps(row,ensure_ascii=False)+"\n")
 with (OUT/"alur-english_candidates.csv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
 print(f"Wrote {len(rows):,} unique Alur candidates")
if __name__=="__main__":main()
