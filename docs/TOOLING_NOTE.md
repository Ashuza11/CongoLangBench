# Phase 0 tooling note: `africa-bitext-builder`

## What it does

`africa-bitext-builder` is a Python library for discovering African-language Bible translations and building verse-aligned parallel or monolingual CSV corpora. It exposes two main components:

- `LanguageRegistry`: resolves an ISO code and returns available translation versions plus public-domain status.
- `CorpusBuilder`: downloads aligned verse rows for a source and target language, with optional version IDs, row limits, sampling, and random seeds.

The package retrieves its catalogue and text from external services. Its output is a useful acquisition starting point, not automatically a reviewed benchmark: we still need to validate language identity, source edition, licence, duplicates, alignment, and domain.

## Installation tested

- Package version: `0.1.13`
- Python: `3.10.12`
- Required package dependencies include `pandas>=2.0.0` and `huggingface-hub>=0.20.0`.
- It was installed into the existing project `venv/` with:

```bash
source venv/bin/activate
python -m pip install africa-bitext-builder
```

The repository `venv/` is linked to a shared environment from the neighboring Africompling project. Do not assume it is isolated until the environment layout is cleaned up.

## Registry smoke test

The package currently resolves these project codes:

| Code | Result |
|---|---|
| `lin` | Lingala |
| `ktu` | Kituba (Democratic Republic of Congo) |
| `lua` | Luba-Lulua |
| `swc` | Congo Swahili |
| `shr` | Shi/Mashi |
| `nnb` | Kinandi/Ndandi |
| `flr` | Fuliiru |
| `tbt` | Tembo |
| `hav` | Havu |
| `nyj` | Nyanga |
| `hke` | Not found in the current registry |
| `leg`, `lea` | Not found in the current registry |

The missing codes must not be treated as unsupported languages. They require a different source workflow or a future package-registry contribution.

## Mashi smoke test

A five-row build succeeded using:

- source language: `shr`
- source version: `3953` — *BIBLIYA NTAGATIFU OMU MASHI*
- target language: `fr`
- target version: `93` — *Bible Segond 1910*
- `limit=5`, `sample=True`, `seed=42`

The output is a CSV with the columns:

```text
verse_key,shr,fr
```

The sample was written to `/tmp/congolang_mashi_smoke.csv` and contains verse keys such as `GEN.29.24`. This confirms that the package can provide a useful Mashi–French acquisition route, but it does not replace the repository’s richer provenance schema or native-speaker review.

## Decision

Use the package as an optional acquisition and discovery adapter for languages it recognizes, especially the four national-language tracks. Keep the current source-specific extractors as the reference for provenance and quality control. For `hke`, `leg`, and `lea`, use dedicated source adapters and community/source outreach unless the package registry gains verified entries.
