"""Summarize the frozen benchmark volume before model inference."""
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "benchmark_freeze.csv"
PROMPT = ROOT / "evaluations" / "prompts" / "translation_v1.txt"
OUTPUT = ROOT / "docs" / "EVALUATION_VOLUME.md"


def main() -> None:
    template = PROMPT.read_text(encoding="utf-8").strip()
    with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        tracks = list(csv.DictReader(handle))

    directions = 2
    records = 0
    input_chars = 0
    input_words = 0
    prompt_chars = 0
    prompt_words = 0
    by_reference: dict[str, int] = {}

    for track in tracks:
        benchmark = ROOT / track["benchmark_csv"]
        with benchmark.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != int(track["benchmark_pairs"]):
            raise ValueError(f"Count mismatch for {track['iso_code']}")

        by_reference[track["reference_language"]] = (
            by_reference.get(track["reference_language"], 0) + len(rows)
        )
        records += len(rows) * directions
        for row in rows:
            for source, source_language, target_language in (
                (row["source_text"], track["reference_language"], track["language"]),
                (row["target_text"], track["language"], track["reference_language"]),
            ):
                prompt = template.format(
                    source_language=source_language,
                    target_language=target_language,
                    input_text=source,
                )
                input_chars += len(source)
                input_words += len(source.split())
                prompt_chars += len(prompt)
                prompt_words += len(prompt.split())

    payload = {
        "language_tracks": len(tracks),
        "directions": directions,
        "requests_per_model": records,
        "input_characters_per_model": input_chars,
        "input_whitespace_tokens_per_model": input_words,
        "prompt_characters_per_model": prompt_chars,
        "prompt_whitespace_tokens_per_model": prompt_words,
        "reference_language_frozen_pairs": dict(sorted(by_reference.items())),
    }
    lines = [
        "# Evaluation volume",
        "",
        "Generated from the frozen `v1` benchmark and prompt `translation_v1`.",
        "These are exact record/character/whitespace-token counts, not provider",
        "billing-token estimates. Provider tokenizers must be measured during the",
        "smoke test before approving a full-run budget.",
        "",
        f"- Language tracks: **{len(tracks):,}**",
        f"- Directions per track: **{directions}**",
        f"- Requests per model: **{records:,}**",
        f"- Prompt characters per model: **{prompt_chars:,}**",
        f"- Prompt whitespace tokens per model: **{prompt_words:,}**",
        "",
        "## Frozen pairs by reference language",
        "",
        "| Reference language | Pairs |",
        "|---|---:|",
    ]
    lines.extend(f"| {language} | {count:,} |" for language, count in sorted(by_reference.items()))
    lines.extend(("", "## Machine-readable summary", "", "```json", json.dumps(payload, indent=2), "```", ""))
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {records:,} requests/model summary to {OUTPUT}")


if __name__ == "__main__":
    main()
