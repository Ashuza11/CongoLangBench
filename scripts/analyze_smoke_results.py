"""Validate a private smoke run and publish aggregate, text-free diagnostics."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import statistics
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "benchmark_freeze.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def score_summary(rows: list[dict], direction: str) -> dict[str, float]:
    selected = [row for row in rows if row["direction"] == direction]
    bleu = [row["bleu"] for row in selected]
    chrf = [row["chrf"] for row in selected]
    return {
        "groups": len(selected),
        "bleu_mean": statistics.mean(bleu),
        "bleu_median": statistics.median(bleu),
        "chrf_mean": statistics.mean(chrf),
        "chrf_median": statistics.median(chrf),
        "chrf_q1": percentile(chrf, 0.25),
        "chrf_q3": percentile(chrf, 0.75),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "docs" / "results" / "GEMMA4_SMOKE_V1.md",
    )
    parser.add_argument(
        "--scores-output",
        type=Path,
        default=ROOT / "docs" / "results" / "gemma4_smoke_v1_scores.csv",
    )
    args = parser.parse_args()
    run_dir = args.run_dir if args.run_dir.is_absolute() else ROOT / args.run_dir
    report = args.report if args.report.is_absolute() else ROOT / args.report
    scores_output = (
        args.scores_output if args.scores_output.is_absolute() else ROOT / args.scores_output
    )

    metadata = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))
    predictions = read_jsonl(run_dir / "predictions.jsonl")
    score_source = run_dir / "smoke_scores.csv"
    raw_scores = read_csv(score_source)
    manifest = read_csv(MANIFEST)
    by_iso = {row["iso_code"]: row for row in manifest}
    expected_directions = {"reference_to_congolese", "congolese_to_reference"}

    prediction_keys = [
        (row["iso_code"], row["direction"], row["record_id"]) for row in predictions
    ]
    if len(prediction_keys) != len(set(prediction_keys)):
        raise ValueError("Duplicate prediction keys found")
    if len(predictions) != int(metadata["requests"]):
        raise ValueError("Prediction count does not match run metadata")
    expected_groups = {(iso, direction) for iso in by_iso for direction in expected_directions}
    actual_groups = {(row["iso_code"], row["direction"]) for row in raw_scores}
    if actual_groups != expected_groups:
        raise ValueError("Score coverage does not match the 47-track manifest")

    scores = []
    for row in raw_scores:
        scores.append({
            **row,
            "examples": int(row["examples"]),
            "empty_predictions": int(row["empty_predictions"]),
            "bleu": float(row["bleu_smoke"]),
            "chrf": float(row["chrf_plus_plus_smoke"]),
            "region": by_iso[row["iso_code"]]["region_group"],
            "track": by_iso[row["iso_code"]]["track"],
        })
    if sum(row["examples"] for row in scores) != len(predictions):
        raise ValueError("Scored example count does not match predictions")

    elapsed = [float(row["elapsed_seconds"]) for row in predictions]
    generated = [int(row["generated_tokens"]) for row in predictions]
    output_lengths = [len(row["prediction"]) for row in predictions]
    actual_empty = sum(not row["prediction"].strip() for row in predictions)
    multiline = sum("\n" in row["prediction"] for row in predictions)
    capped = sum(value >= int(metadata["max_new_tokens"]) for value in generated)
    capped_rows = [
        row for row in predictions
        if int(row["generated_tokens"]) >= int(metadata["max_new_tokens"])
    ]
    capped_directions = Counter(row["direction"] for row in capped_rows)
    capped_languages = {row["iso_code"] for row in capped_rows}
    repeated_within_group = 0
    group_predictions: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in predictions:
        group_predictions[(row["iso_code"], row["direction"])].append(row["prediction"])
    for values in group_predictions.values():
        repeated_within_group += len(values) - len(set(values))

    direction_summaries = {
        direction: score_summary(scores, direction) for direction in sorted(expected_directions)
    }
    paired = defaultdict(dict)
    for row in scores:
        paired[row["iso_code"]][row["direction"]] = row["chrf"]
    reference_advantage = [
        values["congolese_to_reference"] - values["reference_to_congolese"]
        for values in paired.values()
    ]

    regional: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in scores:
        regional[(row["region"], row["direction"])].append(row["chrf"])

    archive_line = "Not supplied"
    if args.archive:
        archive = args.archive if args.archive.is_absolute() else ROOT / args.archive
        archive_line = f"`{sha256(archive)}`"
    lines = [
        "# Gemma 4 all-language smoke test — v1",
        "",
        "> This is a three-example pipeline smoke test, not a final model or language ranking.",
        "> Scores have very high sampling variance and must not support comparative quality claims.",
        "",
        "## Run identity",
        "",
        f"- Model: `{metadata['model_id']}`",
        f"- Model revision: `{metadata['model_revision']}`",
        f"- Repository commit: `{metadata['repository_commit']}`",
        f"- Benchmark / prompt: `{metadata['benchmark_version']}` / `{metadata['prompt_version']}`",
        f"- Hardware: {metadata['gpu']}; {metadata['quantization']}",
        f"- PyTorch: `{metadata['torch_version']}`",
        f"- Completed: {metadata['completed_at_utc']}",
        f"- Original result archive SHA-256: {archive_line}",
        "",
        "## Integrity and completion",
        "",
        f"- Languages: **{metadata['language_tracks']} / 47**",
        f"- Language-direction groups: **{len(scores)} / 94**",
        f"- Predictions: **{len(predictions)} / {metadata['requests']}**",
        f"- Examples per group: **{metadata['rows_per_direction']}**",
        f"- Empty predictions: **{actual_empty}**",
        f"- Duplicate prediction keys: **{len(prediction_keys) - len(set(prediction_keys))}**",
        f"- Outputs reaching the {metadata['max_new_tokens']}-token cap: **{capped}**",
        f"  ({capped / len(predictions) * 100:.1f}%; "
        f"{capped_directions['reference_to_congolese']} reference-to-Congolese, "
        f"{capped_directions['congolese_to_reference']} Congolese-to-reference; "
        f"{len(capped_languages)} languages affected)",
        f"- Multiline outputs: **{multiline}**",
        f"- Repeated outputs within a three-row group: **{repeated_within_group}**",
        "",
        "All 47 languages and both directions completed with exact record coverage. Raw",
        "predictions remain under the Git-ignored `evaluations/runs/` directory because",
        "they contain model output produced from restricted inputs.",
        "",
        "## Runtime diagnostics",
        "",
        f"- Summed generation time: **{sum(elapsed) / 60:.1f} minutes**",
        f"- Median request time: **{statistics.median(elapsed):.2f} seconds**",
        f"- 95th-percentile request time: **{percentile(elapsed, 0.95):.2f} seconds**",
        f"- Generated tokens: **{sum(generated):,} total**, median **{statistics.median(generated):.0f}**, maximum **{max(generated)}**",
        f"- Output length: median **{statistics.median(output_lengths):.0f} characters**, maximum **{max(output_lengths):,}**",
        "",
        "## Aggregate metric diagnostics",
        "",
        "| Direction | Groups | BLEU mean | BLEU median | chrF++ mean | chrF++ median | chrF++ IQR |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for direction, summary in direction_summaries.items():
        lines.append(
            f"| `{direction}` | {summary['groups']} | {summary['bleu_mean']:.2f} | "
            f"{summary['bleu_median']:.2f} | {summary['chrf_mean']:.2f} | "
            f"{summary['chrf_median']:.2f} | {summary['chrf_q1']:.2f}–{summary['chrf_q3']:.2f} |"
        )
    lines.extend([
        "",
        f"Across the 47 paired tracks, Congolese-to-reference chrF++ exceeded the",
        f"reverse direction by a mean of **{statistics.mean(reference_advantage):.2f}** points",
        f"and a median of **{statistics.median(reference_advantage):.2f}** points. This is a",
        "hypothesis for the full run, not a conclusion: French/English generation is",
        "expected to be easier for a broadly pretrained model, and the smoke sample is tiny.",
        "",
        "## Regional chrF++ diagnostics",
        "",
        "| Registry group | Direction | Languages | Mean | Median |",
        "|---|---|---:|---:|---:|",
    ])
    for (region, direction), values in sorted(regional.items()):
        lines.append(
            f"| {region} | `{direction}` | {len(values)} | "
            f"{statistics.mean(values):.2f} | {statistics.median(values):.2f} |"
        )

    lines.extend(["", "## Highest and lowest smoke groups", ""])
    for direction in sorted(expected_directions):
        selected = sorted(
            (row for row in scores if row["direction"] == direction),
            key=lambda row: row["chrf"],
            reverse=True,
        )
        lines.extend([
            f"### `{direction}`",
            "",
            "| Diagnostic band | Language | ISO | chrF++ | BLEU |",
            "|---|---|---:|---:|---:|",
        ])
        for label, subset in (("Higher", selected[:5]), ("Lower", selected[-5:])):
            for row in subset:
                lines.append(
                    f"| {label} | {row['language']} | `{row['iso_code']}` | "
                    f"{row['chrf']:.2f} | {row['bleu']:.2f} |"
                )
        lines.append("")

    lines.extend([
        "## Interpretation and next gate",
        "",
        "The smoke run validates the end-to-end Colab path: private upload, checksum",
        "verification, deterministic 4-bit inference, checkpointing, complete coverage,",
        "scoring, and result export. Before a full 1,500-row run, inspect capped, multiline,",
        "and unusually long outputs privately. The 16.7% cap rate, concentrated in",
        "reference-to-Congolese generation, is a blocking quality-control issue rather than",
        "a harmless runtime detail. Then run a larger 25–50-row pilot to obtain",
        "stable runtime and failure-rate estimates. Final reporting must use the full frozen",
        "set and preserve direction, model revision, quantization, and hardware metadata.",
        "",
    ])
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")
    scores_output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(score_source, scores_output)
    print(f"Validated {len(predictions)} predictions and wrote {report}")
    print(f"Published aggregate score table to {scores_output}")


if __name__ == "__main__":
    main()
