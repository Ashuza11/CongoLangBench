"""Prepare local French--Lega-Shabunda bitext from the official web reader."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/lega-shabunda-lea/data/raw/web"
OUT = ROOT / "language_resources/lega-shabunda-lea/data/processed"
FRENCH = ROOT / "language_resources/mashi-shr/data/raw/shr-fr-v3953-v93.csv"
BASE = "https://media.ipsapps.org/lea/osa/bible"

# The reader prefixes the standard 66-book order with one non-scripture item,
# so canonical book number N is stored as N+1.
BOOKS = [
    ("GEN", 50), ("EXO", 40), ("LEV", 27), ("NUM", 36), ("DEU", 34),
    ("JOS", 24), ("JDG", 21), ("RUT", 4), ("1SA", 31), ("2SA", 24),
    ("1KI", 22), ("2KI", 25), ("1CH", 29), ("2CH", 36), ("EZR", 10),
    ("NEH", 13), ("EST", 10), ("JOB", 42), ("PSA", 150), ("PRO", 31),
    ("ECC", 12), ("SNG", 8), ("ISA", 66), ("JER", 52), ("LAM", 5),
    ("EZK", 48), ("DAN", 12), ("HOS", 14), ("JOL", 3), ("AMO", 9),
    ("OBA", 1), ("JON", 4), ("MIC", 7), ("NAM", 3), ("HAB", 3),
    ("ZEP", 3), ("HAG", 2), ("ZEC", 14), ("MAL", 4), ("MAT", 28),
    ("MRK", 16), ("LUK", 24), ("JHN", 21), ("ACT", 28), ("ROM", 16),
    ("1CO", 16), ("2CO", 13), ("GAL", 6), ("EPH", 6), ("PHP", 4),
    ("COL", 4), ("1TH", 5), ("2TH", 3), ("1TI", 6), ("2TI", 4),
    ("TIT", 3), ("PHM", 1), ("HEB", 13), ("JAS", 5), ("1PE", 5),
    ("2PE", 3), ("1JN", 5), ("2JN", 1), ("3JN", 1), ("JUD", 1),
    ("REV", 22),
]


def clean(value: str) -> str:
    return re.sub(
        r"\s+", " ", unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    ).strip()


def chapter_filename(book_index: int, book: str, chapter: int) -> str:
    return f"Lega-{book_index + 2:02d}-{book}-{chapter:03d}.html"


def fetch(filename: str) -> tuple[str, str]:
    cache = RAW / filename
    if cache.exists():
        return filename, cache.read_text(encoding="utf-8")
    response = requests.get(f"{BASE}/{filename}", timeout=60)
    response.raise_for_status()
    RAW.mkdir(parents=True, exist_ok=True)
    cache.write_text(response.text, encoding="utf-8")
    return filename, response.text


def verse_text(marker: Tag) -> str:
    chunks = []
    node = marker.next_sibling
    while node is not None:
        if isinstance(node, Tag) and node.name == "span" and "v" in node.get("class", []):
            break
        if isinstance(node, NavigableString):
            chunks.append(str(node))
        elif isinstance(node, Tag):
            classes = node.get("class", [])
            identifier = node.get("id", "")
            if "vsp" not in classes and not identifier.startswith("bookmarks"):
                chunks.append(node.get_text(" ", strip=True))
        node = node.next_sibling
    return clean(" ".join(chunks))


def parse_chapter(filename: str, html: str) -> dict[str, str]:
    match = re.fullmatch(r"Lega-\d+-(\w+)-(\d+)\.html", filename)
    if not match:
        raise ValueError(filename)
    book, chapter = match.group(1), int(match.group(2))
    soup = BeautifulSoup(html, "html.parser")
    verses = {}
    for marker in soup.select("span.v"):
        number = clean(marker.get_text(" ", strip=True))
        text = verse_text(marker)
        if number.isdigit() and text:
            reference = f"{book}.{chapter}.{int(number)}"
            verses[reference] = clean(f'{verses.get(reference, "")} {text}')
    return verses


def french_verses() -> dict[str, str]:
    verses = {}
    with FRENCH.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            reference, text = clean(row["verse_key"]), clean(row["fr"])
            if reference and text:
                verses[reference] = text
    return verses


def main() -> None:
    filenames = [
        chapter_filename(book_index, book, chapter)
        for book_index, (book, chapter_count) in enumerate(BOOKS)
        for chapter in range(1, chapter_count + 1)
    ]
    pages = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(fetch, filename): filename for filename in filenames}
        for completed, future in enumerate(as_completed(futures), 1):
            filename, html = future.result()
            pages[filename] = html
            if completed % 50 == 0 or completed == len(filenames):
                print(f"Fetched/verified {completed:,}/{len(filenames):,} chapters", flush=True)

    target = {}
    for filename in filenames:
        target.update(parse_chapter(filename, pages[filename]))
    source = french_verses()
    rows = []
    seen = set()
    for reference, lega in target.items():
        french = source.get(reference)
        pair = (french, lega)
        if not french or pair in seen:
            continue
        seen.add(pair)
        record_id = hashlib.sha256(f"lea-fr\0{french}\0{lega}".encode()).hexdigest()[:16]
        rows.append(
            {
                "language": "Lega-Shabunda",
                "iso_code": "lea",
                "variety": "Lega-Shabunda / Pangi (DRC)",
                "region": "Maniema / South Kivu",
                "source": "Mikanda Zili mu Idagi official web reader / French Louis Segond 1910",
                "source_url": f"{BASE}/",
                "retrieved_at": "2026-08-25",
                "record_id": record_id,
                "reference": reference,
                "source_text": french,
                "target_language": "Lega-Shabunda",
                "target_text": lega,
                "unit_type": "verse",
                "domain": "religious",
                "licence": "copyrighted / redistribution not authorized",
                "review_status": "verified_source_restricted",
                "quality_flags": "evaluation_only_not_publishable",
                "notes": "Authentic complete DRC edition aligned by USFM verse ID; text remains Git-ignored and separate from Lega-Mwenga.",
            }
        )
    if not rows:
        raise RuntimeError("No aligned rows produced")
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "lega-shabunda-french_candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "lega-shabunda-french_candidates.jsonl").open(
        "w", encoding="utf-8"
    ) as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Lega-Shabunda verses: {len(target):,}")
    print(f"French reference verses: {len(source):,}")
    print(f"Wrote {len(rows):,} unique aligned pairs")


if __name__ == "__main__":
    main()
