"""Audit processed bitext against the central language registry.

The audit reads local processed CSV files, including Git-ignored restricted
tracks, and writes publication-safe counts, checksums, and readiness metadata.
It never copies or publishes source text.
"""
from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "languages.csv"
MANIFEST = ROOT / "registry" / "curation_readiness.csv"
REPORT = ROOT / "docs" / "CURATION_STATUS.md"
REQUIRED = {
    "language", "iso_code", "variety", "region", "source", "source_url",
    "retrieved_at", "record_id", "reference", "source_text",
    "target_language", "target_text", "unit_type", "domain", "licence",
    "review_status", "quality_flags", "notes",
}


@dataclass
class FileAudit:
    path: Path
    iso_code: str
    rows: int
    empty_pairs: int
    duplicate_ids: int
    duplicate_pairs: int
    schema_ok: bool
    sha256: str
    reference_language: str

    @property
    def structurally_ready(self) -> bool:
        return (
            self.rows > 0
            and self.empty_pairs == 0
            and self.duplicate_ids == 0
            and self.duplicate_pairs == 0
            and self.schema_ok
        )


def audit_file(path: Path) -> FileAudit:
    ids: set[str] = set()
    pair_hashes: set[bytes] = set()
    iso_codes: Counter[str] = Counter()
    rows = empty_pairs = duplicate_ids = duplicate_pairs = 0
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        schema_ok = REQUIRED <= fields
        for row in reader:
            rows += 1
            iso_codes[(row.get("iso_code") or "").strip()] += 1
            record_id = (row.get("record_id") or "").strip()
            source = (row.get("source_text") or "").strip()
            target = (row.get("target_text") or "").strip()
            if not source or not target:
                empty_pairs += 1
            if not record_id or record_id in ids:
                duplicate_ids += 1
            ids.add(record_id)
            pair_hash = hashlib.sha256(f"{source}\0{target}".encode()).digest()[:16]
            if pair_hash in pair_hashes:
                duplicate_pairs += 1
            pair_hashes.add(pair_hash)
    iso_code = iso_codes.most_common(1)[0][0] if iso_codes else ""
    name = path.name.lower()
    reference_language = "French" if "french" in name else "English" if "english" in name else "unspecified"
    # Release per-row indexes before hashing large corpus files. Reading the
    # entire file with ``read_bytes`` here previously caused avoidable memory
    # spikes on the multi-million-row audit.
    del ids, pair_hashes
    digest = hashlib.sha256()
    with path.open("rb") as binary_handle:
        for chunk in iter(lambda: binary_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return FileAudit(
        path=path,
        iso_code=iso_code,
        rows=rows,
        empty_pairs=empty_pairs,
        duplicate_ids=duplicate_ids,
        duplicate_pairs=duplicate_pairs,
        schema_ok=schema_ok and len(iso_codes) == 1,
        sha256=digest.hexdigest(),
        reference_language=reference_language,
    )


def select_file(candidates: list[FileAudit], expected: int) -> FileAudit | None:
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda item: (
            item.rows != expected,
            not item.structurally_ready,
            abs(item.rows - expected),
            str(item.path),
        ),
    )


def main() -> None:
    processed = sorted(ROOT.glob("language_resources/*/data/processed/*.csv"))
    by_iso: dict[str, list[FileAudit]] = defaultdict(list)
    print(f"Auditing {len(processed):,} processed CSV files", flush=True)
    for index, path in enumerate(processed, 1):
        result = audit_file(path)
        if result.iso_code:
            by_iso[result.iso_code].append(result)
        if index % 10 == 0 or index == len(processed):
            print(f"Audited {index:,}/{len(processed):,} files", flush=True)

    with REGISTRY.open(encoding="utf-8-sig", newline="") as handle:
        registry_rows = list(csv.DictReader(handle))
    active = [
        row for row in registry_rows
        if "backlog" not in row["track"].lower()
        and int(row["current_pairs"]) >= int(row["target_pairs"])
    ]

    manifest_rows = []
    for row in active:
        expected = int(row["current_pairs"])
        audit = select_file(by_iso.get(row["iso_code"], []), expected)
        issues = []
        if audit is None:
            issues.append("processed_csv_missing")
        else:
            if audit.rows != expected:
                issues.append(f"registry_count_mismatch:{expected}!={audit.rows}")
            if not audit.schema_ok:
                issues.append("schema_invalid")
            if audit.empty_pairs:
                issues.append(f"empty_pairs:{audit.empty_pairs}")
            if audit.duplicate_ids:
                issues.append(f"duplicate_ids:{audit.duplicate_ids}")
            if audit.duplicate_pairs:
                issues.append(f"duplicate_pairs:{audit.duplicate_pairs}")
        publication = "restricted_local" if "restricted" in row["status"] else "publishable_or_metadata_qualified"
        manifest_rows.append({
            "language": row["language"],
            "iso_code": row["iso_code"],
            "track": row["track"],
            "region_group": row["region_group"],
            "target_pairs": row["target_pairs"],
            "registry_pairs": row["current_pairs"],
            "processed_csv": "" if audit is None else str(audit.path.relative_to(ROOT)),
            "actual_pairs": "" if audit is None else audit.rows,
            "reference_language": "" if audit is None else audit.reference_language,
            "publication_handling": publication,
            "sha256": "" if audit is None else audit.sha256,
            "status": "ready_for_freeze" if not issues else "needs_attention",
            "issues": ";".join(issues),
        })

    fields = list(manifest_rows[0])
    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(manifest_rows)

    ready = [row for row in manifest_rows if row["status"] == "ready_for_freeze"]
    restricted = [row for row in ready if row["publication_handling"] == "restricted_local"]
    total_pairs = sum(int(row["actual_pairs"]) for row in ready)
    regions = Counter(row["region_group"] for row in ready)
    lines = [
        "# Curation readiness status",
        "",
        "This report is generated by `scripts/audit_curation_readiness.py`. It",
        "checks every active above-target registry track against its local processed",
        "CSV without publishing restricted text.",
        "",
        "## Summary",
        "",
        f"- Active above-target tracks audited: **{len(manifest_rows):,}**",
        f"- Structurally ready for freeze: **{len(ready):,}**",
        f"- Tracks needing attention: **{len(manifest_rows) - len(ready):,}**",
        f"- Restricted local tracks: **{len(restricted):,}**",
        f"- Total validated processed pairs: **{total_pairs:,}**",
        "",
        "A `ready_for_freeze` result means the processed CSV exists, matches the",
        "registry count, contains the common required schema, and has no empty pairs,",
        "duplicate record IDs, or duplicate text pairs. It does not mean benchmark",
        "splits or model evaluations have already been created.",
        "",
        "## Ready tracks by registry group",
        "",
    ]
    lines.extend(f"- {region}: {count}" for region, count in sorted(regions.items()))
    lines.extend([
        "",
        "## Track manifest",
        "",
        "| Language | ISO | Group | Pairs | Reference | Handling | Status |",
        "|---|---:|---|---:|---|---|---|",
    ])
    for row in manifest_rows:
        lines.append(
            f"| {row['language']} | `{row['iso_code']}` | {row['region_group']} | "
            f"{row['actual_pairs'] or '—'} | {row['reference_language'] or '—'} | "
            f"{row['publication_handling']} | {row['status']} |"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Ready: {len(ready):,}/{len(manifest_rows):,} tracks; {total_pairs:,} validated pairs")
    if len(ready) != len(manifest_rows):
        for row in manifest_rows:
            if row["status"] != "ready_for_freeze":
                print(f"NEEDS ATTENTION {row['iso_code']}: {row['issues']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
