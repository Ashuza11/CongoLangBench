"""Align and normalize the complete open Yombe--French eBible coverage."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/yombe-yom/data/raw"
OUT = ROOT / "language_resources/yombe-yom/data/processed"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def read_vpl(archive: Path, member: str) -> dict[str, str]:
    verses = {}
    with zipfile.ZipFile(archive) as bundle:
        text = bundle.read(member).decode("utf-8-sig")
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split(" ", 2)
        if len(parts) == 3 and clean(parts[2]):
            reference = f"{parts[0]} {parts[1]}"
            verses[reference] = clean(parts[2])
    return verses


def main() -> None:
    yombe = read_vpl(RAW / "yom_vpl.zip", "yom_vpl.txt")
    french = read_vpl(RAW / "fraLSG_vpl.zip", "fraLSG_vpl.txt")
    rows, seen = [], set()
    for reference in yombe.keys() & french.keys():
        pair = (french[reference], yombe[reference])
        if pair in seen:
            continue
        seen.add(pair)
        rid = hashlib.sha256(f"yom-fr\0{pair[1]}\0{pair[0]}".encode()).hexdigest()[:16]
        rows.append({
            "language": "Yombe", "iso_code": "yom", "variety": "Kiyombe (DRC)",
            "region": "Western DRC / Kongo Central",
            "source": "Biblica Open Yombe 2002 / French Louis Segond 1910",
            "source_url": "https://ebible.org/Scriptures/details.php?id=yom",
            "retrieved_at": "2026-08-23", "record_id": rid,
            "reference": reference, "source_text": pair[0],
            "target_language": "Yombe", "target_text": pair[1],
            "unit_type": "verse", "domain": "religious", "licence": "CC BY-SA 4.0",
            "review_status": "verified_source", "quality_flags": "",
            "notes": "Original Yombe work copyright © 2002 Biblica, Inc.; derivative formatting normalized and Biblica trademark omitted; aligned with public-domain French Louis Segond 1910.",
        })
    rows.sort(key=lambda row: row["reference"])

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "yombe-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "yombe-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Yombe candidates")


if __name__ == "__main__":
    main()
