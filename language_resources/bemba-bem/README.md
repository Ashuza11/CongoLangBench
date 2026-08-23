# Bemba (`bem`)

## Curation status

Bemba replaces Sanga in the current Southeastern DRC/Katanga top five because
this phase requires languages with usable bitext. The source contains 381,297
English--Bemba rows from MT560/OPUS under CC BY 4.0. The complete source
Parquet is tracked; large normalized CSV and JSONL exports are reproducible
locally.

The source dataset is labelled Zambia. Bemba is also spoken in southeastern
Katanga, so this is retained as an authentic cross-border track and never
presented as a DRC-specific edition. Processed rows carry both
`cross_border_variety` and `mt560_mixed_provenance` flags.

- [Acquisition metadata](metadata/mt560.md)
- [Preparation script](scripts/prepare_mt560.py)
- [Source dataset](https://huggingface.co/datasets/michsethowusu/english-bemba_sentence-pairs_mt560)

Sanga remains documented in the source-acquisition backlog and can be restored
to a later expansion when permissioned or open `sng` bitext becomes available.
