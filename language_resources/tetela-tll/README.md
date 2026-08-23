# Tetela (`tll`)

## Curation status

The tracked source contains 222,225 English--Tetela rows from the MT560/OPUS
collection under CC BY 4.0. The dataset is explicitly labelled as Tetela from
the Democratic Republic of the Congo. The preparation script normalizes the
complete source and retains all 222,212 unique, non-empty pairs.

Generated standard-schema CSV and JSONL files remain local because they are
large and reproducible from the tracked Parquet.

- [Acquisition metadata](metadata/mt560.md)
- [Preparation script](scripts/prepare_mt560.py)
- [Source dataset](https://huggingface.co/datasets/michsethowusu/english-tetela_sentence-pairs_mt560)

The Tetela Bible edition indexed by `africa-bitext-builder` remains excluded
because the package marks it as copyrighted. The open MT560 source is used
instead.
