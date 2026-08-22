# CLEAR Global French--Nande kits

- Source: [CLEAR Global Gamayun kits](https://huggingface.co/datasets/CLEAR-Global/Gamayun-kits)
- Mirror: [Mozilla Data Collective](https://mozilladatacollective.com/datasets/cmoskn32a00vhmj07prz6k5ng)
- Licence: CC BY 4.0; attribution to CLEAR Global required
- Retrieval date: 2026-08-22
- Raw rows: 5,000 (`kit5k`) + 10,000 (`kit10k`)
- Raw `kit5k` SHA-256: `24701fbcb1f529b4ef59acaa11a0ab3700373701f1c948efc242671cee4e919a`
- Raw `kit10k` SHA-256: `a1571c4d3df0dfae6a7b740d199b973fb57d07adf5bd4501f0c9a677740b8832`
- Processed unique non-empty pairs: 14,949

The two kits are independent selections rather than cumulative releases.
Normalization applies Unicode NFC, replaces non-breaking spaces, collapses
whitespace, removes empty pairs, and deduplicates exact normalized pairs across
both kits. All remaining rows are retained and published in CSV and JSONL.

French source sentences originate from Tatoeba. Nande translations were
produced by professional and volunteer translators from Translators without
Borders / CLEAR Global. Cite CLEAR Global and the Gamayun paper as requested by
the dataset card.
