"""Prepare local French--Kanyok bitext from the official jw.org reader.

The downloaded HTML and derived text are intentionally Git-ignored because
jw.org does not grant an open redistribution licence for this material.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[3]
RESOURCE = ROOT / "language_resources" / "kanyok-kny"
RAW = RESOURCE / "data" / "raw" / "jworg"
OUT = RESOURCE / "data" / "processed"
FRENCH = ROOT / "language_resources" / "mashi-shr" / "data" / "raw" / "shr-fr-v3953-v93.csv"
BASE = "https://www.jw.org/kny/cilamin-cya-mikand/bibl/nwt/books"

# Canonical book code, jw.org slug, and chapter count.
BOOKS = [
    ("MAT", "matewus", 28),
    ("MRK", "mark", 16),
    ("LUK", "luuk", 24),
    ("JHN", "jah", 21),
    ("ACT", "myand-yilongel-bapostol", 28),
    ("TIT", "tiit", 3),
]


def clean(value: str) -> str:
    return re.sub(
        r"\s+", " ", unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    ).strip()


def fetch(book: str, slug: str, chapter: int) -> tuple[str, int, str]:
    cache = RAW / f"{book}.{chapter}.html"
    if cache.exists():
        return book, chapter, cache.read_text(encoding="utf-8")
    response = requests.get(
        f"{BASE}/{slug}/{chapter}/",
        headers={"User-Agent": "CongoLangBitextEval/1.0"},
        timeout=60,
    )
    response.raise_for_status()
    RAW.mkdir(parents=True, exist_ok=True)
    cache.write_text(response.text, encoding="utf-8")
    return book, chapter, response.text


def parse_chapter(book: str, chapter: int, html: str) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    verses = {}
    for marker in soup.select("span.verse[id]"):
        identifier = marker.get("id", "")
        match = re.fullmatch(r"v\d{2}(\d{3})(\d{3})", identifier)
        if not match or int(match.group(1)) != chapter:
            continue
        fragment = BeautifulSoup(str(marker), "html.parser")
        for unwanted in fragment.select(
            ".chapterNum, .verseNum, .footnoteLink, .xrefLink, .crossReferenceLink"
        ):
            unwanted.decompose()
        text = clean(fragment.get_text(" ", strip=True))
        if text:
            verses[f"{book}.{chapter}.{int(match.group(2))}"] = text
    return verses


def french_verses() -> dict[str, str]:
    if not FRENCH.exists():
        raise FileNotFoundError(
            f"French reference corpus not found: {FRENCH}. Restore the local "
            "Africa Corpus source before running this extractor."
        )
    verses = {}
    with FRENCH.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            reference, text = clean(row["verse_key"]), clean(row["fr"])
            if reference and text:
                verses[reference] = text
    return verses


def main() -> None:
    chapters = [
        (book, slug, chapter)
        for book, slug, chapter_count in BOOKS
        for chapter in range(1, chapter_count + 1)
    ]
    pages = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(fetch, *chapter) for chapter in chapters]
        for completed, future in enumerate(as_completed(futures), 1):
            book, chapter, html = future.result()
            pages[(book, chapter)] = html
            if completed % 25 == 0 or completed == len(chapters):
                print(f"Fetched/verified {completed:,}/{len(chapters):,} chapters", flush=True)

    target = {}
    for book, _slug, chapter_count in BOOKS:
        for chapter in range(1, chapter_count + 1):
            target.update(parse_chapter(book, chapter, pages[(book, chapter)]))

    source = french_verses()
    rows = []
    seen = set()
    for reference, kanyok in target.items():
        french = source.get(reference)
        pair = (french, kanyok)
        if not french or pair in seen:
            continue
        seen.add(pair)
        record_id = hashlib.sha256(f"kny-fr\0{french}\0{kanyok}".encode()).hexdigest()[:16]
        rows.append(
            {
                "language": "Kanyok",
                "iso_code": "kny",
                "variety": "Kanyok / Kanyoka (DRC)",
                "region": "Kasai--Lomami",
                "source": "Official jw.org Kanyok book set / French Louis Segond 1910",
                "source_url": f"{BASE}/",
                "retrieved_at": "2026-08-26",
                "record_id": record_id,
                "reference": reference,
                "source_text": french,
                "target_language": "Kanyok",
                "target_text": kanyok,
                "unit_type": "verse",
                "domain": "religious",
                "licence": "copyrighted / redistribution not authorized",
                "review_status": "verified_source_restricted",
                "quality_flags": "evaluation_only_not_publishable",
                "notes": "Authentic DRC Kanyok text aligned by canonical verse ID; raw and derived text remain Git-ignored.",
            }
        )

    if len(rows) < 1500:
        raise RuntimeError(f"Only {len(rows):,} aligned pairs; 1,500 required")
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    csv_path = OUT / "kanyok-french_candidates.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "kanyok-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Kanyok verses: {len(target):,}")
    print(f"French reference verses: {len(source):,}")
    print(f"Wrote {len(rows):,} unique aligned pairs")
    print("SHA-256:", hashlib.sha256(csv_path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
