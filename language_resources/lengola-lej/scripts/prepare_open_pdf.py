"""Extract and align all usable Lengola verses from the open source PDF."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

import requests
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "language_resources/lengola-lej/data"
RAW = BASE / "raw"
OUT = BASE / "processed"
PDF_URL = "https://doc-files.bibleineverylanguage.org/1735919439_1230981.pdf"
ULT_URL = "https://git.door43.org/unfoldingWord/en_ult/archive/master.zip"
PDF_PATH = RAW / "lengola-open-bible.pdf"
ULT_PATH = RAW / "en_ult-master.zip"
BOOKS = {
    "Haggai": "HAG",
    "Mark": "MRK",
    "Luke": "LUK",
    "John": "JHN",
    "Acts": "ACT",
    "Romans": "ROM",
    "1 Corinthians": "1CO",
    "2 Corinthians": "2CO",
    "Galatians": "GAL",
    "Philippians": "PHP",
    "Colossians": "COL",
    "1 Thessalonians": "1TH",
    "1 Timothy": "1TI",
    "2 Timothy": "2TI",
    "Titus": "TIT",
    "Philemon": "PHM",
    "James": "JAS",
    "1 Peter": "1PE",
    "2 Peter": "2PE",
    "1 John": "1JN",
    "2 John": "2JN",
    "3 John": "3JN",
    "Jude": "JUD",
}
BAD_TEXT = ("Conflict Parsing Error", "<<<<<<<", "=======", ">>>>>>>")


def clean(value: str) -> str:
    return re.sub(
        r"\s+", " ", unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    ).strip()


def download(url: str, path: Path) -> None:
    if path.exists():
        return
    response = requests.get(url, timeout=180)
    response.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.content)


def strip_usfm(value: str) -> str:
    value = re.sub(r"\\f\s.*?\\f\*", " ", value, flags=re.DOTALL)
    value = re.sub(r"\\x\s.*?\\x\*", " ", value, flags=re.DOTALL)
    value = re.sub(r"\\w\s+([^|\\]+)\|[^\\]*?\\w\*", r"\1", value)
    value = re.sub(r"\\zaln-[se](?:\s+[^\\]*)?\\\*", " ", value)
    value = re.sub(r"\\[A-Za-z0-9-]+\*?", " ", value)
    return clean(value)


def english_verses(path: Path) -> dict[str, str]:
    verses = {}
    with zipfile.ZipFile(path) as archive:
        members = {
            Path(name).stem.split("-", 1)[-1]: name
            for name in archive.namelist()
            if name.endswith(".usfm")
        }
        for book in BOOKS.values():
            member = members[book]
            content = archive.read(member).decode("utf-8")
            chapter = None
            reference = None
            buffer: list[str] = []

            def flush() -> None:
                if reference:
                    text = strip_usfm("\n".join(buffer))
                    if text:
                        verses[reference] = text

            for line in content.splitlines():
                chapter_match = re.match(r"\\c\s+(\d+)", line)
                verse_match = re.match(r"\\v\s+(\d+)\s*(.*)", line)
                if chapter_match:
                    flush()
                    reference = None
                    buffer = []
                    chapter = int(chapter_match.group(1))
                elif verse_match and chapter is not None:
                    flush()
                    number = int(verse_match.group(1))
                    reference = f"{book}.{chapter}.{number}"
                    buffer = [verse_match.group(2)]
                elif reference:
                    buffer.append(line)
            flush()
    return verses


def lengola_verses(path: Path) -> dict[str, str]:
    """Recover the document's visual reading order from positioned PDF text.

    Verse markers use a six-point superscript baseline. Moving that baseline
    down by 6.3 points and bucketing to the nearest visual line allows inline
    verse markers and their text to be ordered correctly even when two verses
    begin on the same line.
    """
    occurrences: dict[str, list[list[str]]] = defaultdict(list)
    book = None
    chapter = None
    active: list[str] | None = None
    reader = PdfReader(path)
    for page in reader.pages[2:]:
        events = []

        def visitor(text, _cm, tm, _font, font_size):
            value = text.strip()
            size = round(font_size, 1)
            if not value:
                return
            y = tm[5] + (6.3 if size == 6.0 else 0.0)
            events.append((round(y), tm[4], y, size, value))

        page.extract_text(visitor_text=visitor)
        for _line, _x, _y, size, value in sorted(events):
            if size == 18.0 and value in BOOKS:
                book = BOOKS[value]
                chapter = None
                active = None
                continue
            chapter_match = re.fullmatch(r"Chapter\s+(\d+)", value)
            if size == 12.0 and chapter_match:
                chapter = int(chapter_match.group(1))
                active = None
                continue
            if (
                size == 6.0
                and value.isdigit()
                and int(value) < 200
                and book
                and chapter
            ):
                reference = f"{book}.{chapter}.{int(value)}"
                active = []
                occurrences[reference].append(active)
                continue
            if size == 12.0 and active is not None:
                active.append(value)

    result = {}
    for reference, candidates in occurrences.items():
        texts = [clean(" ".join(candidate)) for candidate in candidates]
        texts = [text for text in texts if text and not any(flag in text for flag in BAD_TEXT)]
        if texts:
            result[reference] = max(texts, key=len)
    return result


def main() -> None:
    download(PDF_URL, PDF_PATH)
    download(ULT_URL, ULT_PATH)
    target = lengola_verses(PDF_PATH)
    source = english_verses(ULT_PATH)
    rows = []
    seen = set()
    for reference in sorted(set(target) & set(source)):
        english = source[reference]
        lengola = target[reference]
        pair = (english, lengola)
        if pair in seen:
            continue
        seen.add(pair)
        record_id = hashlib.sha256(
            f"lej-en\0{english}\0{lengola}".encode()
        ).hexdigest()[:16]
        rows.append(
            {
                "language": "Lengola",
                "iso_code": "lej",
                "variety": "Lengola (DRC)",
                "region": "Tshopo / Ubundu",
                "source": "Bible in Every Language Lengola collection / unfoldingWord Literal Text",
                "source_url": PDF_URL,
                "retrieved_at": "2026-08-25",
                "record_id": record_id,
                "reference": reference,
                "source_text": english,
                "target_language": "Lengola",
                "target_text": lengola,
                "unit_type": "verse",
                "domain": "religious",
                "licence": "CC BY-SA 4.0",
                "review_status": "verified_source",
                "quality_flags": "open_publishable_pdf_layout_extraction",
                "notes": "Authentic open text aligned by canonical verse identifier; PDF layout extraction is deterministic and conflict-marked rows are excluded.",
            }
        )

    if len(rows) < 1500:
        raise RuntimeError(f"Only {len(rows)} Lengola pairs were produced")
    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "lengola-english_candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "lengola-english_candidates.jsonl").open(
        "w", encoding="utf-8"
    ) as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows):,} open English--Lengola pairs")


if __name__ == "__main__":
    main()
