"""Build the Aushi--French track from package and open PDF sources."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/aushi-auh/data/raw/auh-fr-v4447-v93.csv"
MARK_PDF = ROOT / "language_resources/aushi-auh/data/raw/aushi-mark-2025.pdf"
FRENCH_REFERENCE = ROOT / "language_resources/aushi-auh/data/raw/french-fr-v93.csv"
OUT = ROOT / "language_resources/aushi-auh/data/processed"


def clean(value: str) -> str:
    value = unicodedata.normalize("NFC", value or "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", value).strip()


def extract_mark() -> list[tuple[str, str]]:
    """Extract verse units from the layout-preserving Aushi Mark PDF."""
    pages = PdfReader(MARK_PDF).pages[2:]
    text = "\n".join(page.extract_text(extraction_mode="layout") or "" for page in pages)
    parts = re.split(r"(?m)^\s*(\d{1,2})\s*$", text)[1:]
    combined = {"4445": "44-45", "4647": "46-47", "2627": "26-27", "2829": "28-29"}
    units: list[tuple[str, str]] = []

    for offset in range(0, len(parts), 2):
        chapter, body = int(parts[offset]), parts[offset + 1]
        markers = list(re.finditer(r"(?<!\d)(\d{1,4})(?=(?:['\"“(]|[^\W\d_]))", body))
        for index, marker in enumerate(markers):
            raw_verse = marker.group(1)
            verse = combined.get(raw_verse, raw_verse)
            start = marker.end()
            end = markers[index + 1].start() if index + 1 < len(markers) else len(body)
            value = body[start:end]
            value = re.sub(r"Page \d+ of 15\s+generated on .*?2025", " ", value)
            value = clean(value)
            if value:
                units.append((f"MRK.{chapter}.{verse}", value))

    if len(units) != 674:
        raise ValueError(f"Expected 674 Aushi Mark units, extracted {len(units)}")
    return units


def french_mark() -> dict[str, str]:
    with FRENCH_REFERENCE.open(encoding="utf-8-sig", newline="") as handle:
        return {
            row["verse_key"]: clean(row["text"])
            for row in csv.DictReader(handle)
            if row["verse_key"].startswith("MRK.")
        }


def main() -> None:
    rows, seen = [], set()
    with RAW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = clean(row["verse_key"])
            aushi, french = clean(row["auh"]), clean(row["fr"])
            if not key or not aushi or not french or (aushi, french) in seen:
                continue
            seen.add((aushi, french))
            rid = hashlib.sha256(f"auh-fr\0{aushi}\0{french}".encode()).hexdigest()[:16]
            rows.append({
                "language": "Aushi", "iso_code": "auh",
                "variety": "Aushi (Zambia source; cross-border DRC candidate)",
                "region": "Southeastern DRC / Zambia border zone",
                "source": "Aushi Bible Translation Project / French Louis Segond 1910",
                "source_url": "https://preview.open.bible/bibles/aushi-bible-translation-project",
                "retrieved_at": "2026-08-22", "record_id": rid,
                "reference": key, "source_text": french,
                "target_language": "Aushi", "target_text": aushi,
                "unit_type": "verse", "domain": "religious",
                "licence": "CC BY-SA 4.0", "review_status": "verified_source",
                "quality_flags": "cross_border_variety;below_1500_target",
                "notes": "Aushi edition provided by The Word for the World International for Zambia; aligned with public-domain French Segond 1910.",
            })

    french = french_mark()
    for key, aushi in extract_mark():
        chapter, verse = key.split(".")[1:]
        keys = [f"MRK.{chapter}.{part}" for part in verse.split("-")]
        french_text = clean(" ".join(french[item] for item in keys))
        if not french_text or (aushi, french_text) in seen:
            continue
        seen.add((aushi, french_text))
        rid = hashlib.sha256(f"auh-fr\0{aushi}\0{french_text}".encode()).hexdigest()[:16]
        rows.append({
            "language": "Aushi", "iso_code": "auh",
            "variety": "Aushi (Zambia source; cross-border DRC candidate)",
            "region": "Southeastern DRC / Zambia border zone",
            "source": "Bible in Every Language Aushi Mark / French Louis Segond 1910",
            "source_url": "https://doc-files.bibleineverylanguage.org/auh-reg-mrk_lbo_1c_c_chapter_clf.pdf",
            "retrieved_at": "2026-08-22", "record_id": rid,
            "reference": key, "source_text": french_text,
            "target_language": "Aushi", "target_text": aushi,
            "unit_type": "verse", "domain": "religious",
            "licence": "CC BY-SA 4.0", "review_status": "verified_source",
            "quality_flags": "cross_border_variety;pdf_extraction",
            "notes": "Aushi Mark ©2022 Wycliffe Associates; PDF generated 2025. French Segond 1910 is public domain. Combined references preserve source units.",
        })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "aushi-french_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "aushi-french_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} unique Aushi candidates")


if __name__ == "__main__":
    main()
