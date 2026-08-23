# Songe (`sop`)

## Curation status

The tracked source contains 51,070 English--Songe rows from the MT560/OPUS
collection under CC BY 4.0. The dataset is explicitly labelled as Songe from
the Democratic Republic of the Congo. The preparation script normalizes the
complete source and retains all 51,069 unique, non-empty pairs.

Generated standard-schema CSV and JSONL files remain local because they are
large and reproducible from the tracked Parquet.

- [Acquisition metadata](metadata/mt560.md)
- [Preparation script](scripts/prepare_mt560.py)
- [Source dataset](https://huggingface.co/datasets/michsethowusu/english-songe_sentence-pairs_mt560)
