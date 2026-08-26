"""Build open English--Pende bitext from Door43 repositories."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[3]
RESOURCE = ROOT / "language_resources" / "pende-pem"
RAW = RESOURCE / "data" / "raw"
OUTPUT = RESOURCE / "data" / "processed"
DOOR43 = "https://git.door43.org"
EN_ULT = f"{DOOR43}/unfoldingWord/en_ult/archive/master.zip"

BOOKS = [
    "mrk",
    "1th",
    "2th",
    "1ti",
    "2ti",
    "tit",
    "phm",
    "jas",
    "1pe",
    "2pe",
    "1jn",
    "2jn",
    "3jn",
    "jud",
]

BOOK_CODES = {
    "mrk": "MRK",
    "1th": "1TH",
    "2th": "2TH",
    "1ti": "1TI",
    "2ti": "2TI",
    "tit": "TIT",
    "phm": "PHM",
    "jas": "JAS",
    "1pe": "1PE",
    "2pe": "2PE",
    "1jn": "1JN",
    "2jn": "2JN",
    "3jn": "3JN",
    "jud": "JUD",
}

FAMILIES = [
    {
        "variety": "Gipende Gungu",
        "owner": "parfait-ayanou",
        "prefix": "pem-x-gipendegu",
        "books": BOOKS,
    },
    {
        "variety": "Gipende Ganga",
        "owner": "parfait-ayanou",
        "prefix": "pem-x-gipendega",
        "books": [book for book in BOOKS if book != "jas"],
    },
]


def clean(text: str) -> str:
    text = re.sub(r"\\f\s.*?\\f\*", " ", text, flags=re.S)
    text = re.sub(r"\\x\s.*?\\x\*", " ", text, flags=re.S)
    text = re.sub(r"\\[A-Za-z0-9+_-]+\*?", " ", text)
    return re.sub(
        r"\s+",
        " ",
        unicodedata.normalize("NFC", text).replace("\u00a0", " "),
    ).strip()


def download(session: requests.Session, url: str, destination: Path) -> Path:
    if destination.exists():
        return destination
    response = session.get(url, timeout=120)
    response.raise_for_status()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)
    return destination


def parse_usfm(content: str, book: str) -> dict[str, str]:
    chapter = None
    verses: dict[str, str] = {}
    markers = list(re.finditer(r"\\(c|v)\s+([^\s]+)", content))
    for index, marker in enumerate(markers):
        kind, value = marker.group(1), marker.group(2)
        end = markers[index + 1].start() if index + 1 < len(markers) else len(content)
        if kind == "c":
            chapter = value
            continue
        if chapter is None:
            continue
        text = clean(content[marker.end():end])
        if text:
            verses[f"{book}.{chapter}.{value}"] = text
    return verses


def english_verses(archive: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.namelist():
            match = re.search(r"(?:^|/)(?:\d+-)?([1-3]?[A-Z]{2,3})\.usfm$", member)
            if not match:
                continue
            book = match.group(1)
            content = bundle.read(member).decode("utf-8-sig")
            result.update(parse_usfm(content, book))
    return result


def target_verses(archive: Path, book: str) -> dict[str, str]:
    result: dict[str, str] = {}
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.namelist():
            match = re.search(r"/(\d{2,3})/(\d{2,3})\.txt$", member)
            if not match:
                continue
            chapter = str(int(match.group(1)))
            content = bundle.read(member).decode("utf-8-sig")
            for verse_match in re.finditer(r"\\v\s+([^\s]+)\s*", content):
                start = verse_match.end()
                next_match = re.search(r"\\v\s+[^\s]+\s*", content[start:])
                end = start + next_match.start() if next_match else len(content)
                verse = verse_match.group(1)
                text = clean(content[start:end])
                if text:
                    result[f"{book}.{chapter}.{verse}"] = text
    return result


def main() -> None:
    session = requests.Session()
    session.headers["User-Agent"] = "CongoLangBitextEval/1.0"
    english_archive = download(session, EN_ULT, RAW / "en_ult-master.zip")
    english = english_verses(english_archive)
    entries: list[dict[str, str]] = []

    for family in FAMILIES:
        for short_book in family["books"]:
            repo = f"{family['prefix']}_{short_book}_text_reg"
            url = f"{DOOR43}/{family['owner']}/{repo}/archive/master.zip"
            archive = download(session, url, RAW / f"{repo}.zip")
            book = BOOK_CODES[short_book]
            verses = target_verses(archive, book)
            for reference, target_text in verses.items():
                if reference in english:
                    entries.append(
                        {
                            "family": family["variety"],
                            "repo_url": f"{DOOR43}/{family['owner']}/{repo}",
                            "reference": reference,
                            "target_text": target_text,
                        }
                    )
            print(
                f"{book} / {family['variety']}: {len([e for e in entries if e['family'] == family['variety']]):,} target verses collected"
            )

    rows = []
    seen_pairs = set()
    for entry in sorted(entries, key=lambda item: (item["reference"], item["family"], item["target_text"])):
        pair = (english[entry["reference"]], entry["target_text"])
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        record_id = hashlib.sha256(
            f"pem-pende-en\0{entry['family']}\0{pair[0]}\0{pair[1]}".encode()
        ).hexdigest()[:16]
        rows.append(
            {
                "language": "Phende / Pende",
                "iso_code": "pem",
                "variety": entry["family"],
                "region": "Kasai / Kwilu transition",
                "source": "Door43 open Pende varieties / English ULT",
                "source_url": entry["repo_url"],
                "retrieved_at": "2026-08-25",
                "record_id": record_id,
                "reference": entry["reference"],
                "source_text": pair[0],
                "target_language": entry["family"],
                "target_text": pair[1],
                "unit_type": "verse",
                "domain": "religious",
                "licence": "CC BY-SA 4.0",
                "review_status": "verified_source",
                "quality_flags": "",
                "notes": "Aligned by shared canonical verse ID; original work available at https://door43.org/.",
            }
        )

    if len(rows) < 1500:
        raise RuntimeError(f"Only {len(rows):,} aligned pairs; 1,500 required")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    csv_path = OUTPUT / "pende-english_candidates.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (OUTPUT / "pende-english_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows):,} unique English--Pende pairs")
    print("SHA-256:", hashlib.sha256(csv_path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
