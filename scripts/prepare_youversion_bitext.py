"""Prepare restricted local French bitext from structured YouVersion pages.

Only metadata and this reproducible extractor belong in Git. Cached pages and
derived text are kept in each language resource's Git-ignored data directory.
"""
from __future__ import annotations

import argparse
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

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.bible.com"
FRENCH_VERSION = 93
FRENCH_ABBREV = "LSG"
CONFIGS = {
    "zimba": {
        "language": "Zimba",
        "iso": "zmb",
        "variety": "Zimba (DRC source)",
        "resource": "zimba-zmb",
        "region": "Maniema",
        "version": 3489,
        "abbrev": "ZMB",
        "starts": [
            "MRK.1", "LUK.1", "GAL.1", "EPH.1", "PHP.1", "1TI.1", "2TI.1",
            "TIT.1", "PHM.1", "1PE.1", "2PE.1", "1JN.1", "2JN.1", "3JN.1",
        ],
    },
    "buyu": {
        "language": "Buyu",
        "iso": "byi",
        "variety": "Buyu (DRC source)",
        "resource": "buyu-byi",
        "region": "Maniema",
        "version": 4568,
        "abbrev": "BYI",
        "starts": ["LUK.1"],
    },
    "holoholo": {
        "language": "Holoholo",
        "iso": "hoo",
        "variety": "Holoholo (edition subvariety unspecified)",
        "resource": "holoholo-hoo",
        "region": "Maniema / Tanganyika transition",
        "version": 4460,
        "abbrev": "HBT",
        "starts": ["MRK.1", "LUK.1", "1PE.1"],
    },
    "kete": {
        "language": "Kete",
        "iso": "kcv",
        "variety": "Kete (Kikete)",
        "resource": "kete-kcv",
        "region": "Kasai / Kete-Kuba region",
        "version": 4467,
        "abbrev": "KBT",
        "starts": ["MRK.1", "LUK.1"],
    },
    "hunde": {
        "language": "Hunde/Kihunde",
        "iso": "hke",
        "variety": "Hunde / Kihunde (DRC)",
        "resource": "hunde-hke",
        "region": "North Kivu / Masisi--Rutshuru",
        "version": 4565,
        "abbrev": "HKE",
        "retrieved_at": "2026-08-26",
        "starts": [
            "MAT.1", "MRK.1", "LUK.1", "JHN.1", "ACT.1", "ROM.1",
            "1CO.1", "2CO.1", "GAL.1", "EPH.1", "PHP.1", "COL.1",
            "1TH.1", "2TH.1", "1TI.1", "2TI.1", "TIT.1", "PHM.1",
            "HEB.1", "JAS.1", "1PE.1", "2PE.1", "1JN.1", "2JN.1",
            "3JN.1", "JUD.1", "REV.1",
        ],
    },
}


def clean(value: str) -> str:
    return re.sub(
        r"\s+", " ", unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    ).strip()


def read_page(session: requests.Session, url: str, cache: Path) -> str:
    if cache.exists():
        return cache.read_text(encoding="utf-8")
    response = session.get(url, timeout=60)
    response.raise_for_status()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(response.text, encoding="utf-8")
    time.sleep(0.15)
    return response.text


def verse_texts(soup: BeautifulSoup) -> dict[str, str]:
    pieces: dict[str, list[str]] = defaultdict(list)
    for node in soup.select("span[data-usfm]"):
        reference = node.get("data-usfm", "").strip()
        content = node.select_one('span[class*="content"]')
        text = clean(content.get_text(" ", strip=True) if content else "")
        if reference.count(".") == 2 and text and text not in pieces[reference]:
            pieces[reference].append(text)
    return {reference: clean(" ".join(parts)) for reference, parts in pieces.items()}


def prepare(name: str) -> None:
    config = CONFIGS[name]
    base = ROOT / "language_resources" / config["resource"] / "data"
    raw = base / "raw" / "youversion"
    output = base / "processed"
    session = requests.Session()
    visited = set()
    rows = []
    seen_pairs = set()
    chapter_count = 0

    for start in config["starts"]:
        path = f'/bible/{config["version"]}/{start}.{config["abbrev"]}'
        while path and path not in visited:
            if chapter_count >= 300:
                raise RuntimeError("Safety limit of 300 chapters reached")
            visited.add(path)
            target_cache = re.sub(r"[^A-Za-z0-9._-]+", "_", path.strip("/"))
            target_html = read_page(
                session, BASE + path, raw / f"target_{target_cache}.html"
            )
            target_soup = BeautifulSoup(target_html, "html.parser")
            chapter = target_soup.select_one("div[data-usfm]")
            if chapter is None:
                print(f'{config["language"]}: unavailable start {path}')
                path = None
                continue
            chapter_ref = chapter.get("data-usfm", "").strip()
            target_verses = verse_texts(target_soup)
            source_url = f"{BASE}/bible/{FRENCH_VERSION}/{chapter_ref}.{FRENCH_ABBREV}"
            source_html = read_page(
                session, source_url, raw / f"french_{chapter_ref}.{FRENCH_ABBREV}.html"
            )
            source_verses = verse_texts(BeautifulSoup(source_html, "html.parser"))
            for reference in target_verses:
                if reference not in source_verses:
                    continue
                french, target = source_verses[reference], target_verses[reference]
                pair = (french, target)
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                record_id = hashlib.sha256(
                    f'{config["iso"]}-fr\0{french}\0{target}'.encode()
                ).hexdigest()[:16]
                rows.append(
                    {
                        "language": config["language"],
                        "iso_code": config["iso"],
                        "variety": config["variety"],
                        "region": config["region"],
                        "source": "Official YouVersion edition / French Louis Segond 1910",
                        "source_url": BASE + path,
                        "retrieved_at": config.get("retrieved_at", "2026-08-25"),
                        "record_id": record_id,
                        "reference": reference,
                        "source_text": french,
                        "target_language": config["language"],
                        "target_text": target,
                        "unit_type": "verse",
                        "domain": "religious",
                        "licence": "copyrighted / redistribution not authorized",
                        "review_status": "verified_source_restricted",
                        "quality_flags": "evaluation_only_not_publishable",
                        "notes": "Authentic official text aligned by shared USFM verse ID; cached pages and derived text remain Git-ignored.",
                        "source_version_id": config["version"],
                    }
                )
            chapter_count += 1
            print(f'{config["language"]}: {chapter_ref} ({len(rows):,} pairs)')
            book, chapter_number = chapter_ref.split(".")
            next_href = (
                f'/bible/{config["version"]}/{book}.{int(chapter_number) + 1}.'
                f'{config["abbrev"]}'
            )
            next_link = target_soup.select_one(f'a[href="{next_href}"]')
            path = next_link.get("href") if next_link else None

    if not rows:
        raise RuntimeError("No aligned rows produced")
    output.mkdir(parents=True, exist_ok=True)
    stem = f'{config["iso"]}-french_candidates'
    fields = list(rows[0])
    with (output / f"{stem}.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (output / f"{stem}.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f'{config["language"]}: wrote {len(rows):,} pairs from {chapter_count} chapters')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("language", choices=CONFIGS)
    args = parser.parse_args()
    prepare(args.language)


if __name__ == "__main__":
    main()
