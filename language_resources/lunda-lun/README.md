# Lunda (`lun`)

## Curation status

The source contains 134,578 English--Lunda rows from the MT560/OPUS collection
under CC BY 4.0. The tracked Parquet preserves the complete source artifact;
the preparation script normalizes and deduplicates all usable pairs.

The dataset card labels this as Lunda from Zambia. Lunda is also spoken across
the DRC--Angola--Zambia border region, so the data is retained as an authentic
cross-border Lunda track. It is not represented as a DRC-specific variety, and
all processed rows carry a `cross_border_variety` flag.

Generated standard-schema CSV and JSONL files remain local because they are
large and reproducible from the tracked Parquet.

- [Acquisition metadata](metadata/mt560.md)
- [Preparation script](scripts/prepare_mt560.py)
- [Source dataset](https://huggingface.co/datasets/michsethowusu/english-lunda_sentence-pairs_mt560)

The two Lunda editions indexed by `africa-bitext-builder` remain excluded from
the public repository because the package marks both as copyrighted.
