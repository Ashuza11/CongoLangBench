# Chokwe (`cjk`)

## Curation status

The tracked source contains 35,767 English--Chokwe rows from the MT560/OPUS
collection under CC BY 4.0. The preparation script normalizes the complete
source and retains all 35,765 unique, non-empty pairs.

The dataset card labels this source as Chokwe from Angola. Chokwe is also
spoken across the Angola--DRC border and in the wider Kasai region, so this is
retained as an authentic cross-border track. It is not represented as a
DRC-specific variety, and every processed row carries a
`cross_border_variety` flag.

Generated standard-schema CSV and JSONL files remain local because they are
large and reproducible from the tracked Parquet.

- [Acquisition metadata](metadata/mt560.md)
- [Preparation script](scripts/prepare_mt560.py)
- [Source dataset](https://huggingface.co/datasets/michsethowusu/english-chokwe_sentence-pairs_mt560)
