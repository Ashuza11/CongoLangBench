# Evaluation model selection

Status: **five-model local matrix selected; full runs pending**

Matrix version: `v2-local-five`

Selection date: 2026-09-03

The benchmark uses five downloadable models so the full evaluation can run on
controlled Colab and Kaggle GPU sessions without hosted inference APIs.

| Model | Role | Evaluation scope |
|---|---|---|
| `google/gemma-4-12B-it` | Current instruction-model baseline | All 47 tracks |
| `swiss-ai/Apertus-8B-Instruct-2509` | Massively multilingual open model | All 47 tracks |
| `google/madlad400-10b-mt` | Translation specialist | Exact tokenizer tags |
| `facebook/nllb-200-3.3B` | Established low-resource MT baseline | Exact NLLB tags |
| `bigscience/bloomz-7b1-mt` | Older multilingual instruction baseline | All 47 tracks zero-shot |

The exact machine-readable settings are in `evaluations/model_matrix.json`.
The model revision resolved during download must be saved in every run.

## Selection rationale

- Gemma preserves continuity with the completed 47-language smoke test.
- Apertus tests whether unusually broad multilingual pretraining improves DRC
  language coverage.
- MADLAD and NLLB provide translation-specific comparisons rather than only
  general instruction models.
- BLOOMZ supplies a historically useful multilingual instruction baseline and
  explicitly includes Lingala and Swahili among its declared languages.
- The licences differ and must be reported: NLLB is non-commercial and BLOOMZ
  uses the BLOOM RAIL licence; the remaining selected models declare Apache 2.0.

## Fair-comparison configuration

- Use benchmark `v1` and both directions.
- Use all 1,500 frozen examples for every included language.
- Disable sampling.
- Use `translation_v1` semantically for causal instruction models.
- Use native target/source tags rather than natural-language prompts for
  translation-specific models.
- Generate at most 512 tokens initially; retry only length-capped outputs once
  with a 768-token ceiling.
- Report unsupported MT language tags as coverage results.
- Never substitute a related standard or regional language tag silently.
- Record model revision, precision, hardware, input/output tokens, elapsed time,
  empty output, and truncation status.

## Execution order

1. Complete Gemma on Colab using resumable private Drive checkpoints.
2. Complete NLLB on its exact supported subset on Kaggle.
3. Complete BLOOMZ over all 47 tracks on Kaggle.
4. Complete MADLAD over its exact supported subset on Kaggle.
5. Complete Apertus over all 47 tracks on Kaggle.
6. Validate and score locally, then publish only aggregate and licence-cleared
   artifacts.

See `docs/FULL_EVALUATION_PLAN.md` for operational details.

## Primary references

- <https://huggingface.co/google/gemma-4-12B-it>
- <https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509>
- <https://huggingface.co/google/madlad400-10b-mt>
- <https://huggingface.co/facebook/nllb-200-3.3B>
- <https://huggingface.co/bigscience/bloomz-7b1-mt>
