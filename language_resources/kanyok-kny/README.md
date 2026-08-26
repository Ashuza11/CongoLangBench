# Kanyok (`kny`)

## Curation status

Kanyok / Kanyoka is a DRC-specific language of the Kasai--Lomami area and the
fifth language selected for the Kasai regional track. The earlier KNYFUL
catalogue lead is still documented, but we now also have an official jw.org
online Bible path with verse-keyed book pages for Matthew, Mark, Luke, John,
Acts, and Titus. The local extractor aligned 4,808 source verses with the
project's French reference and retained 4,788 unique pairs, comfortably above
the 1,500-pair target.

The raw pages and aligned text remain Git-ignored because the source does not
provide an open redistribution licence. The tracked script, source metadata,
counts, and checksum make the local evaluation track reproducible without
publishing the text.

Run from the repository root with the existing virtual environment:

```bash
venv/bin/python -u language_resources/kanyok-kny/scripts/prepare_jworg.py
```

- Unique French--Kanyok pairs: **4,788**
- CSV SHA-256: `3d7c26969eedf7c68cf24f4a54b77ad6bf52425b70714c96bd2f83eb254d3de3`

- [Source inventory](metadata/source_inventory.md)
- [Official jw.org source notes](metadata/official_jworg.md)
- [Permission request template](metadata/permission_request.md)
- [Find.Bible Kanyok catalogue](https://find.bible/languages/kny/)
