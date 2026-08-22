# Nande--French Africa Corpus acquisition

- Source: [AfriSpeech Africa Corpus](https://huggingface.co/datasets/AfriSpeech/africa-corpus)
- Retrieval tool: `africa-bitext-builder` 0.1.13
- Retrieval date: 2026-08-22
- Nande code/version: `nnb`, version `1833` (`KB80`)
- French code/version: `fr`, version `93` (Bible Segond 1910)
- Raw aligned rows: 30,914 (30,915 including the CSV header)
- Raw SHA-256: `95192057ba27819410540b2190118c04f42d5aeccf9ab6236f75001f21675d68`
- Curated sample: 1,500 pairs, deterministic seed 42

The dataset card labels the overall licence as `other` and says its text was
derived from public Bible translations retrieved from YouVersion. It explicitly
asks users to review YouVersion's terms before redistributing derived data. The
package metadata marks Nande version 1833 as non-public-domain; French version
93 is public-domain.

The raw and processed text therefore remain local and Git-ignored. The project
commits only the reproducible preparation script, counts, provenance, and source
identifiers until redistribution permission is confirmed.
