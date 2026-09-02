"""Package the frozen local benchmark files for private Colab upload.

The resulting ZIP may contain restricted text and must never be committed or
published. The archive preserves repository-relative paths so the Colab can
validate every file against registry/benchmark_freeze.csv.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "benchmark_freeze.csv"
DEFAULT_OUTPUT = ROOT / "private_data" / "congolang-benchmark-v1.zip"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output

    with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 47:
        raise ValueError(f"Expected 47 frozen tracks; found {len(rows)}")

    files: list[Path] = []
    total_pairs = 0
    for row in rows:
        path = ROOT / row["benchmark_csv"]
        if not path.is_file():
            raise FileNotFoundError(f"Missing local benchmark: {path}")
        actual_sha = sha256(path)
        if actual_sha != row["benchmark_sha256"]:
            raise ValueError(f"Checksum mismatch for {row['iso_code']}: {actual_sha}")
        files.append(path)
        total_pairs += int(row["benchmark_pairs"])

    output.parent.mkdir(parents=True, exist_ok=True)
    bundle_metadata = {
        "bundle_version": "v1",
        "language_tracks": len(rows),
        "benchmark_pairs": total_pairs,
        "contains_restricted_text": True,
        "publication": "private_runtime_input_only_do_not_publish",
        "manifest_sha256": sha256(MANIFEST),
    }
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(MANIFEST, MANIFEST.relative_to(ROOT))
        for path in files:
            archive.write(path, path.relative_to(ROOT))
        archive.writestr(
            "bundle_metadata.json",
            json.dumps(bundle_metadata, indent=2) + "\n",
        )

    print(f"Created private bundle: {output}")
    print(f"Included {len(rows)} tracks / {total_pairs:,} frozen pairs")
    print(f"Archive SHA-256: {sha256(output)}")
    print("Keep this ZIP private. Upload it directly in the Colab when prompted.")


if __name__ == "__main__":
    main()
