"""Download matching official Kibembe and French EPUB publications locally.

The publication text is authentic but copyrighted. Raw downloads and derived
text remain Git-ignored and are only used for local research/evaluation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import requests

API = "https://b.jw-cdn.org/apis/pub-media/GETPUBMEDIALINKS"
PUBLICATION = "lff"
LANGUAGES = {"BMB": "kibembe", "F": "french"}
ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "language_resources/bembe-bmb/data/raw"


def publication_file(language: str) -> dict:
    response = requests.get(
        API,
        params={
            "output": "json",
            "pub": PUBLICATION,
            "fileformat": "EPUB",
            "alllangs": "0",
            "langwritten": language,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["files"][language]["EPUB"][0]["file"]


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for code, name in LANGUAGES.items():
        metadata = publication_file(code)
        destination = RAW / f"{PUBLICATION}_{code}.epub"
        if not destination.exists():
            with requests.get(metadata["url"], stream=True, timeout=180) as response:
                response.raise_for_status()
                with destination.open("wb") as output:
                    for chunk in response.iter_content(1024 * 1024):
                        if chunk:
                            output.write(chunk)
        digest = hashlib.md5(destination.read_bytes()).hexdigest()
        expected = metadata.get("checksum")
        if expected and digest != expected:
            raise RuntimeError(f"Checksum mismatch for {destination.name}")
        manifest[name] = {
            "language_code": code,
            "publication": PUBLICATION,
            "source_url": metadata["url"],
            "bytes": destination.stat().st_size,
            "md5": digest,
        }
        print(f"Verified {destination.name}: {destination.stat().st_size:,} bytes")
    (RAW / "local_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
