"""Normalize the local restricted Ngiti--French alignment."""
from __future__ import annotations
import csv,hashlib,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];RAW=ROOT/"language_resources/ngiti-niy/data/raw/niy-fr-v1431-v93.csv";OUT=ROOT/"language_resources/ngiti-niy/data/processed"
def clean(v:str)->str:return re.sub(r"\s+"," ",unicodedata.normalize("NFC",v or "").replace("\u00a0"," ")).strip()
def main()->None:
 rows=[];seen=set()
 with RAW.open(encoding="utf-8-sig",newline="") as h:
  for n,r in enumerate(csv.DictReader(h),1):
   key,target,source=clean(r["verse_key"]),clean(r["niy"]),clean(r["fr"]);pair=(target,source)
   if not key or not target or not source or pair in seen:continue
   seen.add(pair);rid=hashlib.sha256(f"niy-fr\0{target}\0{source}".encode()).hexdigest()[:16]
   rows.append({"language":"Ngiti","iso_code":"niy","variety":"Ngiti (DRC/Uganda source)","region":"Ituri / Irumu","source":"UNGBÒTA-ƆWɄ́TÁ TƆ́ BHǓKÙ / French Louis Segond 1910","source_url":"https://huggingface.co/datasets/AfriSpeech/africa-corpus","retrieved_at":"2026-08-25","record_id":rid,"reference":key,"source_text":source,"target_language":"Ngiti","target_text":target,"unit_type":"verse","domain":"religious","licence":"restricted / redistribution not authorized","review_status":"verified_source_restricted","quality_flags":"evaluation_only_not_publishable","notes":"Ngiti version 1431 is marked copyrighted by africa-bitext-builder 0.1.13; text remains Git-ignored.","source_version_id":1431,"source_row":n})
 OUT.mkdir(parents=True,exist_ok=True);fields=list(rows[0]) if rows else []
 with (OUT/"ngiti-french_candidates.jsonl").open("w",encoding="utf-8") as h:
  for row in rows:h.write(json.dumps(row,ensure_ascii=False)+"\n")
 with (OUT/"ngiti-french_candidates.csv").open("w",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
 print(f"Wrote {len(rows):,} local restricted Ngiti candidates")
if __name__=="__main__":main()
