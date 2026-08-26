"""Acquire the remaining Eastern DRC tracks with africa-bitext-builder.

Run this script with the Python environment in which
``africa-bitext-builder`` is installed. Access to the gated
``AfriSpeech/africa-corpus`` dataset is required.
"""
from __future__ import annotations

import csv
from pathlib import Path

from africa_bitext_builder.builder import CorpusBuilder
from africa_bitext_builder.registry import LanguageRegistry


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / ".cache" / "africa-corpus"
TRACKS = [
    ("flr", 2355, "fuliiru-flr", "flr-fr-v2355-v93.csv"),
    ("tbt", 3997, "tembo-tbt", "tbt-fr-v3997-v93.csv"),
    ("nyj", 4564, "nyanga-nyj", "nyj-fr-v4564-v93.csv"),
]


def count_rows(path: Path) -> int:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def main() -> None:
    registry = LanguageRegistry(data_root=str(DATA_ROOT))
    for code, version, resource, filename in TRACKS:
        destination = ROOT / "language_resources" / resource / "data" / "raw" / filename
        builder = CorpusBuilder(
            source_lang=code,
            target_lang="fr",
            source_version_ids=version,
            target_version_ids=93,
            registry=registry,
            data_root=str(DATA_ROOT),
        )
        path = Path(builder.download(destination))
        print(f"{code}: wrote {count_rows(path):,} aligned rows to {path}")


if __name__ == "__main__":
    main()
