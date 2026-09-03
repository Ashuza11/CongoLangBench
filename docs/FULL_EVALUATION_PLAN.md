# Five-model full evaluation plan

Planning date: 2026-09-03

Benchmark: `v1`

Prompt: `translation_v1`

## Objective

Complete reproducible translation evaluations for five locally executable
models. This is a production plan, not another pilot. The completed Gemma smoke
test supplies the pipeline evidence; production inference uses every one of the
1,500 frozen pairs in both directions for every valid model-language track.

## Workload

The benchmark contains 47 language tracks and 70,500 bilingual pairs.

| Unit | Requests |
|---|---:|
| One language, one direction | 1,500 |
| One language, both directions | 3,000 |
| All 47 languages, one model | 141,000 |
| Five-model theoretical maximum | 705,000 |

Gemma, Apertus, and BLOOMZ evaluate all 47 tracks. NLLB and MADLAD evaluate
only tracks with exact model language codes. Unsupported tracks are coverage
results, not failed translations, and must never be assigned a related code
silently.

## Model matrix

| Order | Model | Architecture | Scope | Runtime |
|---:|---|---|---|---|
| 1 | `google/gemma-4-12B-it` | instruction causal | all 47 | Colab, resumable |
| 2 | `facebook/nllb-200-3.3B` | translation seq2seq | exact NLLB tags | Kaggle |
| 3 | `bigscience/bloomz-7b1-mt` | instruction causal | all 47 zero-shot | Kaggle |
| 4 | `google/madlad400-10b-mt` | translation seq2seq | exact `<2...>` tags | Kaggle |
| 5 | `swiss-ai/Apertus-8B-Instruct-2509` | instruction causal | all 47 | Kaggle |

The tracked machine-readable configuration is
`evaluations/model_matrix.json`.

## What the Gemma smoke test established

The smoke run completed 282/282 predictions over every language and
direction with no empty outputs. Sequential T4 inference took 58 summed
generation minutes, proving the data, prompt, authentication, scoring, and
private-upload path.

Forty-seven outputs reached the old 256-token ceiling. Production therefore
uses a 512-token initial ceiling and one deterministic 768-token retry only for
an output that reaches 512. Anything still capped at 768 remains in the result
and is reported as truncated.

## Production protocol

- Frozen benchmark `v1`; exactly 1,500 rows per supported track.
- Both `reference_to_congolese` and `congolese_to_reference` directions.
- Sampling disabled.
- Model-native chat formatting for Gemma and Apertus.
- Plain multilingual instruction for BLOOMZ.
- Native `<2target>` prefixes for MADLAD.
- Native source and forced target tags for NLLB.
- Batched inference ordered by approximate input length.
- Automatic batch division after a CUDA out-of-memory error.
- Immediate append-only checkpoints keyed by language, direction, and record ID.
- Resume validation refuses another model, benchmark version, or unexpected key.

## Platform sequence

### Colab — Gemma

Open `notebooks/gemma4_all_languages_full_evaluation.ipynb`. Upload the private
benchmark ZIP and save predictions directly to private Google Drive. A restart
re-uploads the benchmark, reloads the model, and skips every completed record.
If the Colab allocation ends before 141,000 predictions, resume later; do not
replace completed outputs.

Gemma 4 uses the `AutoModelForMultimodalLM` loader and therefore runs with
Transformers 5.x in this notebook. The separate Kaggle workflow retains its
Transformers 4.x environment for the translation-model implementations.

### Kaggle — four models, one at a time

Open `notebooks/kaggle_local_models_full_evaluation.ipynb` and select one
`MODEL_KEY` in this order:

1. `nllb`
2. `bloomz`
3. `madlad`
4. `apertus`

The runner stops cleanly after ten inference hours so the notebook output can
be saved before the session limit. If incomplete, save the private notebook
version, attach its output to the next private session, and rerun the same model
key. Change model keys only after `run_metadata.json` confirms completion.

## Language-tag policy

The exact NLLB matches in benchmark `v1` are Lingala (`lin_Latn`), Ciluba
(`lua_Latn`), Bemba (`bem_Latn`), and Kikongo (`kon_Latn`). English and French
are the corresponding reference tags. Congo Swahili is not silently mapped to
generic `swh_Latn`, and Kikongo ya Leta is not mapped to `kon_Latn`.

MADLAD coverage is derived from the downloaded tokenizer: the runner accepts a
track only when its exact BCP-47/ISO candidate has a real `<2...>` vocabulary
entry. Lingala uses its BCP-47 code `ln` and Kikongo uses `kg`; no regional
proxy is introduced for Congo Swahili.

## Completion gate

A model completes only when:

- predictions exactly match all expected supported record keys;
- each included language-direction group has 1,500 unique predictions;
- model revision, precision, benchmark, and prompt metadata are consistent;
- empty and truncated output counts are recorded; and
- `scripts/score_full_run.py` accepts the result without missing, duplicate, or
  extra keys.

## Scoring and reporting

Primary automatic metrics are corpus BLEU and chrF++ with SacreBLEU signatures.
Report language-level results, macro averages, direction, reference language,
national/regional/Kivu group, failures, truncations, coverage, runtime, and GPU
metadata. Add paired bootstrap intervals before comparative publication claims.

Use three comparison views:

1. Gemma, Apertus, and BLOOMZ over all 47 tracks.
2. All five models over their exact common supported subset.
3. NLLB and MADLAD coverage and scores over their complete valid subsets.

## Data governance

Twenty-four tracks contain restricted local text. Private benchmark ZIPs, raw
references, predictions, and result archives remain outside Git. Git may contain
checksums, configurations, aggregate metrics, timing, failure counts, and
publication-cleared examples. A private Kaggle input or notebook output must
never be made public merely to simplify resumption.

## Official model references

- Gemma: <https://huggingface.co/google/gemma-4-12B-it>
- Apertus: <https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509>
- MADLAD: <https://huggingface.co/google/madlad400-10b-mt>
- NLLB: <https://huggingface.co/facebook/nllb-200-3.3B>
- BLOOMZ: <https://huggingface.co/bigscience/bloomz-7b1-mt>
