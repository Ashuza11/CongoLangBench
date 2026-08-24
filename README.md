# CongoLangBitextEval

[![Project Status](https://img.shields.io/badge/status-active_development-brightgreen)](docs/PROJECT_SPEC.md)
[![Task](https://img.shields.io/badge/task-bitext_evaluation-6f42c1)](docs/PROJECT_SPEC.md)
[![Coverage](https://img.shields.io/badge/coverage-27_language_tracks-007ec6)](registry/languages.csv)
[![Data](https://img.shields.io/badge/data-bitext_%7C_lexicons_%7C_corpora-f39c12)](registry/national_sources.csv)
[![Licence](https://img.shields.io/badge/licensing-source_specific-e05d44)](docs/PROJECT_SPEC.md)

CongoLangBitextEval is a reproducible text-evaluation project for languages spoken in the Democratic Republic of Congo. It curates documented bilingual text, validates language and licence provenance, and evaluates language models on comparable translation tasks.

## Current project roadmap

The work is deliberately staged:

1. Complete the four national-language tracks: Lingala, Kikongo ya Leta, Ciluba/Tshiluba, and Congo Swahili.
2. Select and document up to five feasible bitext-supported local languages per major DRC region.
3. Focus on a dedicated Kivu expansion, extending the existing Mashi, Nande, Hunde, Fuliiru, Tembo, Havu, Nyanga, and Lega work.
4. Add further languages whenever credible bitext, provenance, licensing, and review support become available.

The target for each completed language is at least **1,500 curated bilingual sentence pairs**. Model evaluation is intentionally gated until the selected national and regional language datasets have been curated and frozen.

The full plan is in [docs/PROJECT_SPEC.md](docs/PROJECT_SPEC.md).

## Current status

### Mashi prototype

The Mashi track demonstrates the extraction and evaluation workflow. It contains candidate Mashi–French material from eBible Exodus, a contextual dictionary PDF, and murhula.com. The candidates still require linguistic review before they become an official benchmark split.

- [Mashi extraction notebook](notebooks/mashi_data_extraction.ipynb)
- [Open Mashi notebook in Colab](https://colab.research.google.com/github/Ashuza11/CongoLangBench/blob/main/notebooks/mashi_data_extraction.ipynb)
- [Mashi candidate data](language_resources/mashi-shr/data/)
- [Mashi source files](language_resources/mashi-shr/sources/)

### Lingala acquisition

The CLEAR Global Gamayun collection also provides a 5,000-row French–Lingala kit under CC BY 4.0. After removing one exact duplicate and normalizing whitespace, the track contains 4,999 verified-source rows.

- [Raw Lingala bitext](language_resources/lingala-lin/data/raw/)
- [Processed Lingala candidates](language_resources/lingala-lin/data/processed/)
- [Lingala acquisition metadata](language_resources/lingala-lin/metadata/gamayun_kit.md)

### Kikongo ya Leta acquisition

SMOL provides Kituba (`ktu`) sentence and document translations under CC BY 4.0, plus a separate lexicon. Sentence data is being curated separately from the lexicon, and the source’s documented Kituba quality warning is retained in row metadata.

- [Kituba raw data](language_resources/kituba-ktu/data/raw/)
- [Kituba metadata](language_resources/kituba-ktu/metadata/smol.md)
- [Kituba preparation script](language_resources/kituba-ktu/scripts/prepare_smol.py)

### Ciluba/Tshiluba acquisition

The accepted African Languages Lab `multi-open` collection provides the main English--Tshiluba track. After normalization and exact deduplication, it contains 397,971 usable pairs. The raw source artifact is tracked; large processed exports are reproducible locally. The separate SMOL GATITOS lexicon remains supporting data and is not counted as sentence bitext.

- [Ciluba raw lexicon](language_resources/ciluba-lua/data/raw/)
- [Ciluba source metadata](language_resources/ciluba-lua/metadata/smol.md)

### Congo Swahili acquisition

The first national-language acquisition is the CLEAR Global Gamayun Congo Swahili collection:

- 5,000-row kit
- 10,000-row kit
- 10,305-row kit
- 25,305 raw French–`swc` pairs in total
- 25,217 unique exact pairs after initial duplicate inspection
- 25,214 normalized, cross-kit deduplicated verified rows
- CC BY 4.0, with CLEAR Global attribution required

These rows are accepted as supplied from an authentic source and validated by a Congo Swahili speaker. Leakage-safe splitting and evaluation still remain.

- [Raw Congo Swahili bitext](language_resources/congo-swahili-swc/data/raw/)
- [Processed Congo Swahili candidates](language_resources/congo-swahili-swc/data/processed/)
- [Congo Swahili preparation script](language_resources/congo-swahili-swc/scripts/prepare_gamayun.py)
- [Congo Swahili acquisition metadata](language_resources/congo-swahili-swc/metadata/gamayun_kits.md)
- [Congo Swahili source worksheet](language_resources/congo-swahili-swc/README.md)

## National-language source plan

The four national tracks are:

| Language | ISO 639-3 | Target | Current stage |
|---|---:|---:|---|
| Lingala | `lin` | 1,500 curated pairs | Verified source; 4,999 processed |
| Kikongo ya Leta / DRC Kituba | `ktu` | 1,500 curated pairs | Verified source; 2,469 processed |
| Ciluba / Tshiluba | `lua` | 1,500 curated pairs | Verified source; 397,971 processed |
| Congo Swahili | `swc` | 1,500 curated pairs | Verified source; 25,214 processed |

See the [national source table](registry/national_sources.csv) and [national source plan](registry/national_sources.md).

## Regional selection

The provisional regional table contains up to five priority candidates per major region. A candidate is not counted as an active dataset track until a usable bitext source, exact language variety, DRC provenance, licence, and review route are confirmed.

- [Regional candidate shortlist](registry/regional_candidates.csv)
- [Regional selection rules](registry/regional_candidates.md)
- [Central language registry](registry/languages.csv)

The Southeastern DRC/Katanga top five are Kiluba, Tabwa, Bemba, Aushi, and
Lunda. Each now has usable open bitext. Bemba, Aushi, and Lunda use explicitly
labelled cross-border sources; DRC-specific comparison data remains desirable.
Sanga (`sng`) remains in the acquisition backlog because no redistributable
bitext was found.

The Kasai/Central DRC top five are Tshiluba, Tetela, Songe, Ruund, and Kanyok.
Tshiluba reuses the completed national track; Tetela now has 222,212 processed
English pairs, Songe has 51,069, and Ruund has 133,626. Kanyok is DRC-specific
and has a documented complete Bible pending text
acquisition and reuse verification. The Angola-labelled Chokwe resource is no
longer part of the active top five.

- [Kasai top-five plan](registry/kasai_top5.md)

The Western DRC top five are Kituba, Yaka, Kikongo/Koongo, Yansi, and Yombe.
Kituba reuses the completed national track. Yaka has 7,104 French pairs, Yansi
has 7,951 French pairs, and Yombe has 10,408 French pairs. The African
Languages Lab source supplies 330,000 raw English--Kikongo rows and 315,959
unique normalized pairs; its broad Kikongo label is retained because it does
not identify a specific DRC subvariety per row. Pende remains a priority
acquisition backlog after searches across open non-religious corpora found no
downloadable English or French sentence bitext.

- [Western DRC top-five record](registry/western_top5.md)

The Northwestern Congo Basin top five are Mongo/Nkundo, Ngombe, Northern
Ngbandi, Ngbaka, and Lobala. Lingala is not counted because it already belongs
to the national track. Every local track exceeds 1,500 pairs. Ngombe is
publishable open data; Mongo, Northern Ngbandi, Ngbaka, and Lobala are curated
locally from authentic sources but remain Git-ignored because redistribution
is not authorized. Budza and Mbandja remain documented acquisition backlogs.

- [Northwestern Congo Basin top-five record](registry/northwestern_top5.md)

## Repository structure

```text
docs/                       Project specification and tooling notes
notebooks/                  Extraction and evaluation notebooks
language_resources/         Per-language worksheets, data, and sources
registry/                   Language, source, and regional tracking tables
requirements.txt            Reproducible Python dependency list
```

## Reproducibility

Use the existing project environment:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
```

The notebooks can be run locally or in Google Colab. Raw source files must remain separate from processed and benchmark files. Do not use provisional or quarantined rows for final evaluation.

## Data and quality rules

- Keep ISO codes and language varieties explicit; do not merge related varieties silently.
- Preserve source URL, edition, retrieval date, licence, attribution, and contributor information.
- Keep raw, normalized, reviewed, and benchmark files separate.
- Keep native, human-translated, mined, machine-translated, and synthetic text labelled separately.
- Deduplicate overlapping releases before splitting data.
- Split by source/document where necessary to prevent leakage.
- Treat automatic BLEU and chrF++ scores as comparisons, not complete quality judgments.
- Obtain native-speaker or qualified linguistic review for unverified sources; authentic verified datasets may be accepted with documented validation.

## Evaluation

[llm_bitext_evaluation.ipynb](notebooks/llm_bitext_evaluation.ipynb) provides the initial model-evaluation workflow. After the curation milestone, each completed language track should save its model version, prompts, predictions, references, BLEU/chrF++ scores, and error analysis.

## Tooling

Phase 0 investigated [`africa-bitext-builder`](https://pypi.org/project/africa-bitext-builder/). It can discover indexed African-language Bible versions and build verse-aligned CSV corpora, but its output still requires this project’s provenance, licence, language, and human-review checks.

- [Phase 0 tooling note](docs/TOOLING_NOTE.md)
- [Project specification](docs/PROJECT_SPEC.md)
