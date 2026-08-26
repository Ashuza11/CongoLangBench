"""Freeze deterministic 1,500-pair evaluation sets for every ready track.

Benchmark text is written locally under each resource's ``data/benchmark``
directory and is Git-ignored. The publication-safe freeze manifest contains
only paths, counts, algorithms, and checksums.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "registry" / "curation_readiness.csv"
MANIFEST = ROOT / "registry" / "benchmark_freeze.csv"
REPORT = ROOT / "docs" / "BENCHMARK_FREEZE.md"
VERSION = "v1"
SAMPLE_SIZE = 1_500
SELECTION = "sha256(congolang-bitext-eval-v1\\0iso\\0record_id), lowest 1500"


def selection_key(iso_code: str, record_id: str) -> str:
    return hashlib.sha256(
        f"congolang-bitext-eval-v1\0{iso_code}\0{record_id}".encode()
    ).hexdigest()


def freeze(row: dict[str, str]) -> dict[str, str | int]:
    source_path = ROOT / row["processed_csv"]
    with source_path.open(encoding="utf-8-sig", newline="") as handle:
        candidates = list(csv.DictReader(handle))
    if len(candidates) < SAMPLE_SIZE:
        raise RuntimeError(f"{row['iso_code']}: only {len(candidates):,} candidates")
    ranked = sorted(
        candidates,
        key=lambda item: (selection_key(row["iso_code"], item["record_id"]), item["record_id"]),
    )
    selected = ranked[:SAMPLE_SIZE]
    selected.sort(key=lambda item: (item.get("reference", ""), item["record_id"]))
    for item in selected:
        item["benchmark_version"] = VERSION
        item["benchmark_split"] = "eval"

    resource = source_path.parents[2]
    output_dir = resource / "data" / "benchmark"
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{row['iso_code']}-eval-{VERSION}"
    csv_path = output_dir / f"{stem}.csv"
    jsonl_path = output_dir / f"{stem}.jsonl"
    fields = list(selected[0])
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(selected)
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for item in selected:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    return {
        "language": row["language"],
        "iso_code": row["iso_code"],
        "track": row["track"],
        "region_group": row["region_group"],
        "reference_language": row["reference_language"],
        "publication_handling": row["publication_handling"],
        "source_csv": row["processed_csv"],
        "source_pairs": len(candidates),
        "source_sha256": row["sha256"],
        "benchmark_version": VERSION,
        "benchmark_split": "eval",
        "benchmark_pairs": len(selected),
        "selection_algorithm": SELECTION,
        "benchmark_csv": str(csv_path.relative_to(ROOT)),
        "benchmark_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "status": "frozen_local",
    }


def main() -> None:
    if not READINESS.exists():
        raise FileNotFoundError(
            "Run scripts/audit_curation_readiness.py before freezing benchmarks"
        )
    with READINESS.open(encoding="utf-8-sig", newline="") as handle:
        readiness = list(csv.DictReader(handle))
    not_ready = [row for row in readiness if row["status"] != "ready_for_freeze"]
    if not_ready:
        raise RuntimeError(
            "Readiness audit has unresolved tracks: "
            + ", ".join(row["iso_code"] for row in not_ready)
        )

    frozen = []
    for index, row in enumerate(readiness, 1):
        frozen.append(freeze(row))
        print(f"Frozen {row['iso_code']}: {index}/{len(readiness)}", flush=True)

    fields = list(frozen[0])
    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(frozen)

    groups = Counter(row["region_group"] for row in frozen)
    restricted = sum(row["publication_handling"] == "restricted_local" for row in frozen)
    lines = [
        "# Benchmark freeze",
        "",
        f"Benchmark version **{VERSION}** freezes exactly **{SAMPLE_SIZE:,}** evaluation",
        f"pairs for each of **{len(frozen)}** ready language tracks, for a total of",
        f"**{len(frozen) * SAMPLE_SIZE:,}** evaluation pairs.",
        "",
        "The selection is deterministic: records are ranked by",
        f"`{SELECTION}`. Every frozen set is evaluation-only; no training split is",
        "created, so benchmark verses or sentences cannot leak into a project training",
        "partition. Source overlap with external model pretraining remains a documented",
        "limitation, especially for religious-domain datasets.",
        "",
        "All benchmark text is currently Git-ignored. Open-source tracks can be",
        "regenerated from tracked processed data; restricted tracks are reproducible",
        "from their local authorized source workflow. The tracked manifest records",
        "source and frozen-output checksums without redistributing restricted text.",
        "",
        "## Summary",
        "",
        f"- Frozen language tracks: **{len(frozen)}**",
        f"- Evaluation pairs per track: **{SAMPLE_SIZE:,}**",
        f"- Total evaluation pairs: **{len(frozen) * SAMPLE_SIZE:,}**",
        f"- Restricted local tracks: **{restricted}**",
        "",
        "## Tracks by registry group",
        "",
    ]
    lines.extend(f"- {group}: {count}" for group, count in sorted(groups.items()))
    lines.extend([
        "",
        "## Reproduction",
        "",
        "```bash",
        "venv/bin/python -u scripts/audit_curation_readiness.py",
        "venv/bin/python -u scripts/freeze_benchmarks.py",
        "```",
        "",
        "See `registry/benchmark_freeze.csv` for per-language source and benchmark",
        "checksums.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Frozen {len(frozen)} tracks / {len(frozen) * SAMPLE_SIZE:,} evaluation pairs")


if __name__ == "__main__":
    main()
