# Resume the Gemma full evaluation on Modal

This workflow transfers the existing private Colab checkpoint to a private
Modal Volume and resumes the same Gemma model revision and benchmark. It does
not restart completed record IDs.

## Cost guard

The app requests one L40S, two physical CPU cores, and 32 GiB of memory, and
limits inference to 600 minutes (10 hours). At the 2026-09-30 base rates, the
requested GPU, CPU, and memory total approximately **$23.01** for ten hours.
This leaves a buffer within the $30 Starter allowance for image activity,
storage, and pricing variance. Confirm current spend in the Modal dashboard and
set an environment budget before launching.

Do not run a second GPU function concurrently against the same $30 allowance.
The cap protects the budget; it does **not** guarantee that all remaining rows
will finish in one session.

### Why batch size 32 is the default

Numeric-only inspection of the 4,456-row checkpoint found:

- 4,231 ordinary outputs averaged 7.66 generated tokens;
- 225 outputs required the 768-token retry, and 191 still ended at that limit;
- recorded generation time improved from approximately 3.95 seconds per row
  at batch size 8 to 1.45 seconds per row at batch size 32.

The long pathological generations explain much of the slowdown. We retain the
same 512-token initial limit and 768-token retry so this continuation remains
compatible with the existing run. Modal may split a batch automatically after
an out-of-memory error.

## 1. Preserve the Colab checkpoint

Download these private assets to the computer from which the Modal CLI will run:

- `congolang-benchmark-v1.zip`
- either the Drive result archive or its contained
  `gemma4-12b-it-full-v1/predictions.jsonl`

Do not edit or publish either file.

The local archive
`gemma4-12b-it-full-v1-20260930T002643Z-1-001.zip` has been verified to contain
4,456 valid predictions from the expected Gemma revision. It is the checkpoint
to resume—not the older 2,560-row snapshot shown in the Colab log.

## 2. Configure Modal

From the repository root, install and authenticate the CLI:

```bash
venv/bin/python -m pip install -U modal
venv/bin/modal setup
```

Use `python -m pip` here because this repository's legacy `venv/bin/pip`
launcher may still contain a path from the environment in which it was first
created.

In the Modal dashboard, create a secret named `congolang-huggingface` containing
one key, `HF_TOKEN`, with a Hugging Face read token that can access Gemma 4.

Create an environment budget capped at $30 before running paid inference.

## 3. Upload the private inputs once

The uploader accepts the Google Drive ZIP directly:

```bash
venv/bin/modal run deployment/modal_gemma_full.py \
  --action upload \
  --bundle private_data/congolang-benchmark-v1.zip \
  --checkpoint gemma4-12b-it-full-v1-20260930T002643Z-1-001.zip
```

The upload action extracts `predictions.jsonl` in a temporary directory when
needed and validates that every checkpoint row identifies
`google/gemma-4-12B-it` before transferring it. Both files enter the private
`congolang-benchmark-private` Volume. They are not baked into the container
image.

Use `--replace` only when intentionally replacing the Volume checkpoint with a
newer local copy. Never replace a more advanced Modal checkpoint with an older
Colab file.

## 4. Confirm the remote checkpoint

```bash
venv/bin/modal run deployment/modal_gemma_full.py --action status
```

The reported prediction count must be at least the count last printed by
Colab. Stop if it is smaller.

## 5. Run the budget-capped L40S job

```bash
venv/bin/modal run deployment/modal_gemma_full.py \
  --action run \
  --batch-size 32 \
  --max-runtime-minutes 600
```

The runner streams progress, retries smaller batches after CUDA out-of-memory,
and writes each completed batch to the private Volume. Modal also performs
background Volume commits, and the wrapper commits explicitly before exit.

The job stops in either of two states:

- complete at 141,000 predictions with `run_metadata.json`; or
- safely incomplete with `session_state.json`, ready for a later resume.

Do not launch another run while one is active because both processes would
append to the same prediction file.

## 6. Download the private result

Inspect status first, then download the files:

```bash
venv/bin/modal run deployment/modal_gemma_full.py --action status

venv/bin/modal volume get congolang-benchmark-private \
  runs/gemma4-12b-it-full-v1/predictions.jsonl \
  gemma4-full-predictions.jsonl
```

When complete, also download metadata:

```bash
venv/bin/modal volume get congolang-benchmark-private \
  runs/gemma4-12b-it-full-v1/run_metadata.json \
  gemma4-full-run-metadata.json
```

Raw predictions remain private. Only aggregate, text-free scores should enter
Git until every source licence has been checked for publication.

## Official Modal references

- Pricing: <https://modal.com/pricing>
- GPU selection: <https://modal.com/docs/guide/gpu>
- Persistent Volumes: <https://modal.com/docs/guide/volumes>
