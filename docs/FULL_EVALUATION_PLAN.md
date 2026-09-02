# Full multilingual evaluation plan

Planning date: 2026-09-02

Benchmark: `v1`

Prompt: `translation_v1`

## Scope

The frozen benchmark contains 47 language tracks, 1,500 pairs per track, and
two translation directions. A complete run therefore requires:

| Unit | Requests |
|---|---:|
| One language, one direction | 1,500 |
| One language, both directions | 3,000 |
| All 47 languages, one model | 141,000 |
| Four-model core matrix | 564,000 |

The exact prompt volume per model is 36,897,141 characters or 5,906,338
whitespace-delimited tokens. Billing tokens depend on each provider tokenizer
and must be measured in the next pilot.

## What the first Gemma run established

The three-row Gemma smoke test completed all 282 requests on a Tesla T4 in 58
summed generation minutes. Direct linear scaling gives approximately **483 T4
GPU-hours** for the 141,000-request full run before batching, optimization, or
hardware changes. That is about 20 continuous days and is not suitable for a
single ordinary Colab session.

The smoke test also produced 47 outputs at the 256-token ceiling: 45 occurred
in reference-to-Congolese generation. The full run must not start until private
inspection identifies whether these are valid long translations, repetition,
format leakage, or decoding failures. The next pilot should use a 512-token
ceiling, report both output length and finish reason, and require a cap rate
below 1% or a documented language-specific explanation.

## Core model matrix

| Track | Exact model | Execution | Core settings |
|---|---|---|---|
| Open-weight | `google/gemma-4-12B-it` | Private GPU | 4-bit NF4, thinking off, `do_sample=false`, 512 output tokens |
| Google hosted | `gemini-3.7-flash` | Batch API | low thinking, omit unsupported sampling fields, 512 output tokens |
| Anthropic hosted | `claude-sonnet-5` | Message Batches | thinking disabled, omit non-default sampling fields, 512 output tokens |
| OpenAI hosted | `gpt-5.6-sol` | Batch/Responses API | reasoning effort `none`, deterministic setting where supported, 512 output tokens |

An optional cost-sensitivity extension can compare `gpt-5.6-luna` with Sol.
Do not add it until the core four-model matrix is complete.

## Data-governance gate

Twenty-four tracks contain restricted local text. They can be evaluated by a
locally loaded model because the text remains inside the controlled runtime.
Do **not** upload those tracks to a hosted provider merely because API access
exists. For every hosted run, confirm that the source licence permits external
processing and that the chosen provider account has acceptable retention and
training controls. If that gate is not met:

1. run Gemma locally on all 47 tracks;
2. run hosted models only on explicitly cleared tracks; and
3. report the two scopes separately instead of presenting them as the same
   language matrix.

Raw prompts, references, and predictions from restricted tracks remain private.
Only aggregate metrics and text-free diagnostics enter Git.

## Cost envelope for hosted models

Before provider tokenization is measured, use a transparent planning scenario
of **10 million input plus 10 million output tokens per model**. This is close
to the Gemma smoke output extrapolation (about 9.7 million generated tokens),
but it is not a quotation or spending authorization.

| Model | Current standard input/output per MTok | Scenario standard cost | Batch planning cost |
|---|---:|---:|---:|
| `gemini-3.7-flash` | $0.75 / $3.75 | $45 | $22.50 |
| `claude-sonnet-5` | $2 / $10 | $120 | about $60 at the documented 50% batch discount |
| `gpt-5.6-sol` | $4 / $20 | $240 | Verify the account's Batch rate before approval |

Prices are USD, exclude retries and taxes, and can change. Google promotional
pricing is documented through 2026-12-31; OpenAI describes current Sol pricing
as promotional through at least 2026-11-21. Claude batch cost is derived from
its $2/$10 standard price and documented 50% Message Batches discount. Actual
approval must use token counts returned by a 50-row pilot.

Gemma has no per-token API fee, but GPU time is a real cost. The observed
sequential T4 requirement is roughly 483 hours. Record the actual cloud or
Colab price rather than assigning an artificial zero cost.

## Execution phases

### Phase 1 — Diagnose the current Gemma output ceiling

- Privately inspect all 47 capped predictions without copying their text into
  documentation.
- Classify each as valid length, repetition, prompt leakage, wrong language,
  or other generation failure.
- Add finish reason, input tokens, output tokens, and repetition detection to
  the runner.
- Retain prompt `translation_v1`; version any prompt change as a new protocol.

**Exit gate:** no unexplained truncation and a validated output parser.

### Phase 2 — Fifty-row all-language pilot

- Run 50 rows × 47 languages × two directions = **4,700 requests per model**.
- On the measured T4 path, Gemma would take roughly 16 GPU-hours before
  optimization.
- Test safe batching sizes of 2, 4, and 8; do not assume linear speedup.
- For hosted models, record provider billing tokens, failures, refusals,
  latency, finish reasons, and exact cost.
- Compare deterministic reruns on a small fixed subset.

**Exit gate:** 100% record coverage, less than 1% unexplained cap/failure rate,
stable parsing, and an approved full-run budget.

### Phase 3 — Full local Gemma run

- Split the workload into 94 language-direction shards of 1,500 records.
- Checkpoint every prediction and maintain a shard manifest with pending,
  running, complete, failed, and scored states.
- Resume by record ID; never regenerate completed rows silently.
- Prefer a persistent A100/H100 or equivalent job environment over ephemeral
  free Colab. Benchmark throughput before selecting hardware.
- Merge only after each shard has 1,500 unique record IDs and matching dataset,
  prompt, model-revision, and decoding metadata.

### Phase 4 — Hosted batch runs

- Submit only licence-cleared tracks.
- Use provider batch endpoints for cost and operational stability where their
  data-handling terms are acceptable.
- Keep one language-direction per logical shard even if several shards share a
  provider batch file.
- Set spending limits and stop submission when projected cost exceeds the
  approved budget by 10%.
- Save provider request IDs, model IDs, usage, errors, refusals, and raw outputs
  privately.

### Phase 5 — Scoring and analysis

- Require exact prediction coverage before scoring.
- Report BLEU and chrF++ using saved SacreBLEU signatures.
- Add paired bootstrap confidence intervals and direction-level comparisons.
- Separate national, regional, Kivu, reference-language, source-domain, and
  publication-handling analyses.
- Select blinded error-analysis samples before reading model identities.
- Use speaker review for final claims, beginning with Congo Swahili and the
  languages for which qualified reviewers are available.

## Required implementation before full execution

- A batched, sharded Gemma runner suitable for persistent GPU jobs.
- Provider-specific batch exporters/importers for Google, Anthropic, and
  OpenAI, with no credentials stored in the repository.
- A shared run manifest and exact-coverage validator.
- Token/cost accounting based on provider response metadata.
- Finish-reason, refusal, repetition, language-ID, and truncation diagnostics.
- A result merger that refuses mixed model revisions, prompts, or benchmark
  checksums.

## Publication artifacts

Git may contain:

- aggregate score tables;
- model, prompt, benchmark, hardware, and quantization metadata;
- counts, checksums, timing, token usage, cost, and failure categories; and
- text examples only from sources whose licences explicitly allow publication.

Keep private:

- restricted source/reference text;
- raw hosted batch files containing restricted text;
- model outputs derived from restricted inputs; and
- API credentials and provider account identifiers.

## Current official pricing references

- OpenAI GPT-5.6 Sol: <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
- Google Gemini pricing: <https://ai.google.dev/gemini-api/docs/pricing>
- Claude Sonnet 5 pricing: <https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5>
- Claude batch processing: <https://platform.claude.com/docs/en/build-with-claude/batch-processing>
