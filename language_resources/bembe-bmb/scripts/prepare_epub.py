"""Align matching Kibembe and French paragraphs by publication document/pid."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/bembe-bmb/data/raw"
OUT = ROOT / "language_resources/bembe-bmb/data/processed"
EPUBS = {"bmb": RAW / "lff_BMB.epub", "fr": RAW / "lff_F.epub"}


def clean(value: str) -> str:
    return re.sub(
        r"\s+", " ", unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    ).strip()


def paragraphs(epub: Path) -> dict[tuple[str, str], str]:
    rows = {}
    with zipfile.ZipFile(epub) as archive:
        names = {
            name
            for name in archive.namelist()
            if name.startswith("OEBPS/")
            and name.endswith(".xhtml")
            and "-extracted" not in name
            and not name.endswith("cover.xhtml")
        }
        for name in sorted(names):
            doc_id = Path(name).stem
            soup = BeautifulSoup(archive.read(name), "html.parser")
            for element in soup.select("p[data-pid]"):
                for hidden in element.select('[aria-hidden="true"]'):
                    hidden.decompose()
                pid = element.get("data-pid", "").strip()
                text = clean(element.get_text(" ", strip=True))
                if pid and text:
                    rows[(doc_id, pid)] = text
    return rows


def main() -> None:
    source = paragraphs(EPUBS["fr"])
    target = paragraphs(EPUBS["bmb"])
    rows = []
    seen = set()
    for key in sorted(source, key=lambda item: (item[0], int(item[1]))):
        if key not in target:
            continue
        french, kibembe = source[key], target[key]
        pair = (french, kibembe)
        if pair in seen:
            continue
        seen.add(pair)
        doc_id, pid = key
        record_id = hashlib.sha256(
            f"bmb-fr\0{french}\0{kibembe}".encode()
        ).hexdigest()[:16]
        rows.append(
            {
                "language": "Bembe/Kibembe",
                "iso_code": "bmb",
                "variety": "Kibembe (DRC)",
                "region": "Maniema / South Kivu",
                "source": "Enjoy Life Forever matching official EPUBs",
                "source_url": "https://www.jw.org/",
                "retrieved_at": "2026-08-25",
                "record_id": record_id,
                "reference": f"lff:{doc_id}:p{pid}",
                "source_text": french,
                "target_language": "Bembe/Kibembe",
                "target_text": kibembe,
                "unit_type": "paragraph",
                "domain": "religious education",
                "licence": "copyrighted / redistribution not authorized",
                "review_status": "verified_source_restricted",
                "quality_flags": "evaluation_only_not_publishable",
                "notes": "Authentic matching official publication paragraphs aligned by shared document ID and data-pid; text remains Git-ignored.",
            }
        )
    if not rows:
        raise RuntimeError("No matching paragraphs found")
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "bembe-french_candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as output:
        writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "bembe-french_candidates.jsonl").open("w", encoding="utf-8") as output:
        for row in rows:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"French paragraphs: {len(source):,}")
    print(f"Kibembe paragraphs: {len(target):,}")
    print(f"Wrote {len(rows):,} unique aligned pairs")


if __name__ == "__main__":
    main()
