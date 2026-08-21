# CLEAR Global Gamayun Congo Swahili acquisition

## Source

- Dataset: [TWB Parallel Sentence kits — Congo Swahili](https://mozilladatacollective.com/datasets/cmosl07v400w9nu07g3puif2t)
- Mirror: [CLEAR-Global/Gamayun-kits](https://huggingface.co/datasets/CLEAR-Global/Gamayun-kits)
- Configuration: `parallel/swc-fra`
- Language: Congo Swahili (`swc`)
- Translation: French ↔ Congo Swahili
- Licence: CC BY 4.0
- Attribution: CLEAR Global; cite the Gamayun Language Data Kits publication listed on the source page.
- Retrieval date: 2026-08-21

## Raw files

| File | Data rows | SHA-256 |
|---|---:|---|
| `swc-fra-kit5k.tsv` | 5,000 | `0c9081f1c3ee204cb3f31e8ee9db18c3aa554c4706fb95c9401ce06abd261104` |
| `swc-fra-kit10k.tsv` | 10,000 | `2b2053a2b9808f25d6c98b2c6ce78d1a4b11be3a389ded4650e207ec55f69d99` |
| `swc-fra-kit15k.tsv` | 10,305 | `f635c21cca04127169ef4098309167f1516521a98fc0370c2fd16efa198df404` |

The three kits contain 25,305 rows in total. Kit selections are independent; `kit10k` is not a superset of `kit5k`. Each file has `fra`, `swc`, and `swc_clean` columns. `swc_clean` removes parenthetical content where available.

## Initial checks

- No empty cells were found in the three downloaded files.
- There are 88 duplicate exact French–Congo Swahili pairs across the kits.
- There are 25,217 unique exact pairs before any language or quality review.
- French sentences overlap across kits; split assignment must happen after cross-kit deduplication.
- `swc_clean` differs from `swc` in 857 rows; retain both and document which field is evaluated.

These are raw acquired candidates, not yet reviewed benchmark rows. The next steps are cross-kit deduplication, language/quality review, source-aware splitting, and native-speaker validation.

## Processed candidate export

`data/processed/congo-swahili-french_candidates.jsonl` and `.csv` contain **25,214** unique candidates after Unicode/whitespace normalization and cross-kit exact-pair deduplication. The processed rows use the repository-wide metadata schema and remain marked `needs_review`. The `swc_clean` field is used as the evaluation target while the original `swc` value is retained as `target_text_raw`.

The preparation script is [scripts/prepare_gamayun.py](../scripts/prepare_gamayun.py). Run it from the repository root with `venv/bin/python` to regenerate the processed files.
