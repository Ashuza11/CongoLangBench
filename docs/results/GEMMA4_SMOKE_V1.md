# Gemma 4 all-language smoke test — v1

> This is a three-example pipeline smoke test, not a final model or language ranking.
> Scores have very high sampling variance and must not support comparative quality claims.

## Run identity

- Model: `google/gemma-4-12B-it`
- Model revision: `707f0a3b8a3c7ad586ed01e27eafbad8a27dd0f7`
- Repository commit: `473dac16576f68b315d04dd96fe9364a056e5440`
- Benchmark / prompt: `v1` / `translation_v1`
- Hardware: Tesla T4; bitsandbytes_nf4_4bit
- PyTorch: `2.11.0+cu128`
- Completed: 2026-09-02T15:55:47.819930+00:00
- Original result archive SHA-256: `352346d25bd37e72ac242a5cd332a408b59ae8190fb0f8a6fdb3de41c1b4e17a`

## Integrity and completion

- Languages: **47 / 47**
- Language-direction groups: **94 / 94**
- Predictions: **282 / 282**
- Examples per group: **3**
- Empty predictions: **0**
- Duplicate prediction keys: **0**
- Outputs reaching the 256-token cap: **47**
  (16.7%; 45 reference-to-Congolese, 2 Congolese-to-reference; 25 languages affected)
- Multiline outputs: **0**
- Repeated outputs within a three-row group: **0**

All 47 languages and both directions completed with exact record coverage. Raw
predictions remain under the Git-ignored `evaluations/runs/` directory because
they contain model output produced from restricted inputs.

## Runtime diagnostics

- Summed generation time: **58.0 minutes**
- Median request time: **6.37 seconds**
- 95th-percentile request time: **42.99 seconds**
- Generated tokens: **19,399 total**, median **32**, maximum **256**
- Output length: median **116 characters**, maximum **1,254**

## Aggregate metric diagnostics

| Direction | Groups | BLEU mean | BLEU median | chrF++ mean | chrF++ median | chrF++ IQR |
|---|---:|---:|---:|---:|---:|---:|
| `congolese_to_reference` | 47 | 3.80 | 2.15 | 21.47 | 20.20 | 17.46–24.01 |
| `reference_to_congolese` | 47 | 1.09 | 0.48 | 9.00 | 7.62 | 3.99–11.71 |

Across the 47 paired tracks, Congolese-to-reference chrF++ exceeded the
reverse direction by a mean of **12.47** points
and a median of **12.54** points. This is a
hypothesis for the full run, not a conclusion: French/English generation is
expected to be easier for a broadly pretrained model, and the smoke sample is tiny.

## Regional chrF++ diagnostics

| Registry group | Direction | Languages | Mean | Median |
|---|---|---:|---:|---:|
| Central DRC | `congolese_to_reference` | 4 | 22.03 | 22.01 |
| Central DRC | `reference_to_congolese` | 4 | 5.09 | 3.45 |
| DRC-wide | `congolese_to_reference` | 4 | 33.87 | 28.25 |
| DRC-wide | `reference_to_congolese` | 4 | 22.19 | 22.87 |
| Ituri | `congolese_to_reference` | 5 | 17.14 | 17.57 |
| Ituri | `reference_to_congolese` | 5 | 5.31 | 4.30 |
| Kivu | `congolese_to_reference` | 7 | 20.00 | 23.01 |
| Kivu | `reference_to_congolese` | 7 | 9.41 | 9.53 |
| Maniema | `congolese_to_reference` | 5 | 21.09 | 21.02 |
| Maniema | `reference_to_congolese` | 5 | 10.34 | 11.73 |
| Northern DRC | `congolese_to_reference` | 5 | 20.07 | 20.20 |
| Northern DRC | `reference_to_congolese` | 5 | 7.90 | 7.54 |
| Northwestern Congo Basin | `congolese_to_reference` | 5 | 22.15 | 21.51 |
| Northwestern Congo Basin | `reference_to_congolese` | 5 | 6.58 | 2.83 |
| Southeastern DRC | `congolese_to_reference` | 5 | 22.33 | 21.58 |
| Southeastern DRC | `reference_to_congolese` | 5 | 10.35 | 11.81 |
| Tshopo | `congolese_to_reference` | 3 | 16.55 | 17.08 |
| Tshopo | `reference_to_congolese` | 3 | 8.28 | 10.40 |
| Western DRC | `congolese_to_reference` | 4 | 20.52 | 20.85 |
| Western DRC | `reference_to_congolese` | 4 | 5.20 | 4.51 |

## Highest and lowest smoke groups

### `congolese_to_reference`

| Diagnostic band | Language | ISO | chrF++ | BLEU |
|---|---|---:|---:|---:|
| Higher | Congo Swahili | `swc` | 58.95 | 28.25 |
| Higher | Ngbaka | `nga` | 35.15 | 5.94 |
| Higher | Kikongo ya Leta | `ktu` | 33.97 | 13.16 |
| Higher | Aushi | `auh` | 29.35 | 3.44 |
| Higher | Luba-Katanga | `lub` | 28.53 | 13.40 |
| Lower | Tabwa | `tap` | 14.49 | 1.70 |
| Lower | Lombo / Turumbu | `loo` | 13.90 | 1.16 |
| Lower | Kakwa | `keo` | 13.83 | 0.81 |
| Lower | Northern Ngbandi | `ngb` | 10.55 | 0.84 |
| Lower | Nande | `nnb` | 9.34 | 2.46 |

### `reference_to_congolese`

| Diagnostic band | Language | ISO | chrF++ | BLEU |
|---|---|---:|---:|---:|
| Higher | Congo Swahili | `swc` | 37.51 | 5.52 |
| Higher | Lingala | `lin` | 34.04 | 4.92 |
| Higher | Luba-Katanga | `lub` | 19.87 | 7.64 |
| Higher | Mashi | `shr` | 19.14 | 2.04 |
| Higher | Ngbaka | `nga` | 17.19 | 1.21 |
| Lower | Nande | `nnb` | 2.04 | 0.00 |
| Lower | Hunde | `hke` | 2.02 | 0.35 |
| Lower | Mongo | `lol` | 1.82 | 0.56 |
| Lower | Ngiti | `niy` | 1.81 | 0.25 |
| Lower | Ruund | `rnd` | 1.24 | 1.02 |

## Interpretation and next gate

The smoke run validates the end-to-end Colab path: private upload, checksum
verification, deterministic 4-bit inference, checkpointing, complete coverage,
scoring, and result export. Before a full 1,500-row run, inspect capped, multiline,
and unusually long outputs privately. The 16.7% cap rate, concentrated in
reference-to-Congolese generation, is a blocking quality-control issue rather than
a harmless runtime detail. Then run a larger 25–50-row pilot to obtain
stable runtime and failure-rate estimates. Final reporting must use the full frozen
set and preserve direction, model revision, quantization, and hardware metadata.
