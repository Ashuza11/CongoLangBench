# Model evaluation workflow

The curation milestone is complete. Benchmark version `v1` contains 1,500
evaluation-only pairs for each of 47 language tracks. Model inference must use
the frozen local files referenced by `registry/benchmark_freeze.csv`.

## 1. Generate a local evaluation job

```bash
venv/bin/python scripts/prepare_evaluation_job.py lin reference_to_congolese
venv/bin/python scripts/prepare_evaluation_job.py lin congolese_to_reference
```

Use `--limit` only for an explicitly labelled smoke test. Final comparable
runs use all 1,500 frozen records. Smoke and full jobs have distinct filenames,
for example:

```bash
venv/bin/python scripts/prepare_evaluation_job.py lin reference_to_congolese --limit 10
```

The generated JSONL contains the source sentence, reference translation, and
prompt. Jobs are Git-ignored because some tracks contain restricted text.

## 2. Run a model

The production notebooks are:

- `notebooks/gemma4_all_languages_full_evaluation.ipynb` for the resumable
  141,000-request Gemma run on Colab;
- `notebooks/kaggle_local_models_full_evaluation.ipynb` for NLLB, BLOOMZ,
  MADLAD, and Apertus, one model at a time on Kaggle.

Both workflows validate the private benchmark ZIP against the tracked freeze
manifest. They checkpoint by `(iso_code, direction, record_id)` and refuse to
mix model or benchmark versions. NLLB and MADLAD additionally write an exact
language-tag coverage manifest.

Use the proposed, exact identifiers and provider-specific controls in
`evaluations/model_matrix.json`. Send each job's `prompt` to the selected model
with deterministic decoding where the provider supports it. Save one JSONL
prediction per input record:

```json
{"record_id": "...", "prediction": "..."}
```

Do not silently retry with a different model version or prompt. Record the
provider, exact model identifier, access date, decoding parameters, and failed
requests in the run metadata.

## 3. Score predictions

```bash
venv/bin/python scripts/score_predictions.py \
  evaluations/jobs/lin-reference_to_congolese-v1-full.jsonl \
  evaluations/runs/<run-id>/predictions.jsonl \
  evaluations/runs/<run-id>/scores.json
```

Use the exact generated job filename; final jobs end in `-full.jsonl` and
smoke-test jobs end in `-smoke-<count>.jsonl`.

The scorer checks exact record coverage and reports corpus BLEU and chrF++.
Scores are comparative signals, not complete linguistic judgments.

## Fair-comparison rules

- Use the same prompt version across models.
- Evaluate both translation directions where possible.
- Use all 1,500 frozen examples for final results.
- Disable sampling where supported. Do not send unsupported sampling fields;
  record the exact provider-specific settings instead.
- Do not provide demonstrations, dictionaries, or retrieval context in the
  zero-shot baseline.
- Label smoke tests, partial runs, failures, and provider safety refusals.
- Report source-domain and likely pretraining-overlap limitations.

See `docs/MODEL_SELECTION.md` for the proposed matrix and execution order, and
`docs/EVALUATION_VOLUME.md` for the exact request volume per model.

## 4. Validate and score a full run

After a model reports completion, score it locally without publishing raw text:

```bash
venv/bin/python scripts/score_full_run.py \
  --repo-root . \
  --data-root private_data/extracted-benchmark-v1 \
  --run-root evaluations/runs/<model>-full-v1 \
  --output-root evaluations/runs/<model>-full-v1/scored
```

Only the aggregate `scores.csv` and `validation.json` are publication-safe by
default. Review source licences before publishing any example or prediction.
