"""Build publishable French--Lombo bitext from CC BY-SA HTML documents."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "language_resources/lombo-loo/data"
RAW = BASE / "raw"
OUT = BASE / "processed"
FRENCH_VERSION = 93
FRENCH_ABBREV = "LSG"
DOCUMENTS = {
    "MRK": "https://doc-files.bibleineverylanguage.org/loo-reg-mrk_lbo_1c_c_chapter_clf.html",
    "LUK": "https://doc-files.bibleineverylanguage.org/loo-reg-luk_lbo_1c_c_chapter_clf.html",
}


def clean(value: str) -> str:
    return re.sub(
        r"\s+", " ", unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    ).strip()


def get(session: requests.Session, url: str, cache: Path) -> bytes:
    if cache.exists():
        return cache.read_bytes()
    response = session.get(url, timeout=90)
    response.raise_for_status()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(response.content)
    time.sleep(0.15)
    return response.content


def lombo_verses(content: bytes, book: str) -> dict[str, str]:
    soup = BeautifulSoup(content, "html.parser")
    verses = {}
    for chapter in soup.select("div.chapter"):
        marker = chapter.select_one("span.chaptermarker")
        if marker is None or not marker.get_text(strip=True).isdigit():
            continue
        chapter_number = int(marker.get_text(strip=True))
        for verse in chapter.select("span.verse"):
            number = verse.select_one("sup.versemarker")
            if number is None or not number.get_text(strip=True).isdigit():
                continue
            verse_number = int(number.get_text(strip=True))
            number.extract()
            text = clean(verse.get_text(" ", strip=True))
            if text:
                verses[f"{book}.{chapter_number}.{verse_number}"] = text
    return verses


def french_verses(content: bytes) -> dict[str, str]:
    soup = BeautifulSoup(content, "html.parser")
    pieces: dict[str, list[str]] = defaultdict(list)
    for node in soup.select("span[data-usfm]"):
        if not any("verse" in name for name in node.get("class", [])):
            continue
        reference = node.get("data-usfm", "").strip()
        # Verses may be split into several spans around notes or poetry markup.
        # Keep content owned by this exact verse node and exclude note bodies.
        for value in node.select('span[class*="content"]'):
            if value.find_parent(attrs={"data-usfm": True}) is not node:
                continue
            if any(
                any("note" in name for name in parent.get("class", []))
                for parent in value.parents
                if parent is not node
            ):
                continue
            text = clean(value.get_text(" ", strip=True))
            if (
                reference.count(".") == 2
                and text
                and text not in pieces[reference]
            ):
                pieces[reference].append(text)
    return {key: clean(" ".join(value)) for key, value in pieces.items()}


def main() -> None:
    session = requests.Session()
    rows = []
    seen = set()
    for book, url in DOCUMENTS.items():
        target = lombo_verses(
            get(session, url, RAW / f"lombo-{book.lower()}.html"), book
        )
        chapters = sorted({int(reference.split(".")[1]) for reference in target})
        french = {}
        for chapter in chapters:
            reference = f"{book}.{chapter}"
            url_fr = (
                f"https://www.bible.com/bible/{FRENCH_VERSION}/"
                f"{reference}.{FRENCH_ABBREV}"
            )
            french.update(
                french_verses(
                    get(
                        session,
                        url_fr,
                        RAW / "french" / f"{reference}.{FRENCH_ABBREV}.html",
                    )
                )
            )
        for reference, target_text in target.items():
            source_text = french.get(reference, "")
            pair = (source_text, target_text)
            if not source_text or pair in seen:
                continue
            seen.add(pair)
            record_id = hashlib.sha256(
                f"loo-fr\0{source_text}\0{target_text}".encode()
            ).hexdigest()[:16]
            rows.append(
                {
                    "language": "Lombo",
                    "iso_code": "loo",
                    "variety": "Lombo (DRC)",
                    "region": "Tshopo / Congo Basin transition",
                    "source": "Bible in Every Language Lombo documents / French Louis Segond 1910",
                    "source_url": DOCUMENTS[book],
                    "retrieved_at": "2026-08-25",
                    "record_id": record_id,
                    "reference": reference,
                    "source_text": source_text,
                    "target_language": "Lombo",
                    "target_text": target_text,
                    "unit_type": "verse",
                    "domain": "religious",
                    "licence": "CC BY-SA 4.0",
                    "review_status": "verified_source",
                    "quality_flags": "open_publishable",
                    "notes": "Authentic open text aligned to public-domain French by canonical verse identifier; attribution retained in metadata.",
                }
            )

    if len(rows) < 1500:
        raise RuntimeError(f"Only {len(rows)} Lombo pairs were produced")
    rows.sort(key=lambda row: row["reference"])
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "lombo-french_candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "lombo-french_candidates.jsonl").open(
        "w", encoding="utf-8"
    ) as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows):,} open French--Lombo pairs")


if __name__ == "__main__":
    main()
