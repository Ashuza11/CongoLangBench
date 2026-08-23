# Kikongo / Koongo (`kon`)

## Western DRC track

This track uses the accepted `english-kikongo` configuration from African
Languages Lab `multi-open`. The source contains 330,000 raw English--Kikongo
rows. Whitespace normalization, removal of empty rows, and exact pair
deduplication produce **315,959 unique candidates**. All source-authenticated
pairs are retained; the automatic translation-quality score is analysis
metadata only and is not treated as human review.

Kikongo is a major language of Western DRC and the wider Kongo language area.
It is **not** the same track as Kikongo ya Leta / Kituba (`ktu`). The dataset
uses the broad label `kikongo` and does not identify a DRC subvariety for each
row, so the processed metadata preserves that limitation instead of relabelling
the text as a specific DRC variety.

The raw Parquet is tracked. Large normalized CSV and JSONL outputs are
reproducible and Git-ignored:

```bash
venv/bin/python language_resources/kikongo-kon/scripts/prepare_multi_open.py
```

- [Source metadata](metadata/multi_open.md)
- [Dataset card](https://huggingface.co/datasets/African-Languages-Lab/multi-open)
