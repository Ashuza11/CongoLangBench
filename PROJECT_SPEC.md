# CongoLangBitextEval — Project Specification

## 1. Project purpose

Build a reproducible text-evaluation benchmark for languages spoken in the Democratic Republic of Congo (DRC). The first collection program covers a minimum of **1,500 reviewed bilingual sentence pairs per national language** plus up to five feasible bitext-supported local languages per major region. Each completed language track must produce a documented dataset, a repeatable evaluation run, and saved results that can be compared across languages.

The project focuses on text and bitext evaluation. Monolingual corpora, dictionaries, and speech resources may support discovery, normalization, and future work, but they are not counted as bilingual sentence pairs unless they have a valid alignment and reuse permission.

## 2. Scope and language tracks

### Phase 1 — Four national languages

The initial tracks are:

| Language | Target variety | ISO 639-3 | Minimum reviewed bitext |
|---|---|---:|---:|
| Lingala | DRC Lingala | `lin` | 1,500 sentence pairs |
| Kikongo | Kikongo ya Leta / DRC Kituba | `ktu` | 1,500 sentence pairs |
| Ciluba | Tshiluba / Luba-Kasai | `lua` | 1,500 sentence pairs |
| Swahili | Congo Swahili from the DRC | `swc` | 1,500 sentence pairs |

Generic Kongo, generic Standard Swahili, and unrelated Luba or Kikongo varieties must not be silently merged into these tracks. Every record must retain its exact variety and ISO code.

### Phase 1B — Regional top-five language tracks

Alongside the four national languages, identify up to **five local languages per major DRC region** for which a usable bitext source can be identified. A language is selected only when its variety, provenance, licence, and at least one credible bitext route can be documented. Population estimates guide prioritization but do not substitute for data availability or language validation.

The regional shortlist must be based on:

1. population and local importance;
2. geographic coverage and representation gaps;
3. availability of at least one credible bitext source;
4. an identifiable ISO code and language variety;
5. permission or a compatible open licence; and
6. feasibility of native-speaker review.

The shortlist is a research output, not an assumption. Record candidate languages, rejected candidates, evidence, bitext status, and the reason for each decision in `registry/regional_candidates.csv`.

Potential regional groupings to investigate include Western/Greater Kinshasa, Kongo Central, Kasai, Katanga, North Kivu, South Kivu, Ituri, Maniema, and other areas supported by evidence. Boundaries and language membership must be validated against sources and speakers rather than inferred from province names alone.

### Phase 2 — Kivu expansion

After the national-language benchmark and the broader regional top-five selection are complete, focus specifically on the Kivu regions. Extend the existing Mashi, Nande, Hunde, Fuliiru, Tembo, Havu, Nyanga, and Lega work where data is available, and add additional Kivu languages discovered through the regional process. Kivu additions must use the same 1,500-pair target, review rules, and evaluation protocol; they are an expansion of the benchmark, not a replacement for the national or regional tracks.

### Phase 3 — Continuous expansion

Add further Congolese languages whenever credible data is found. New languages follow the same intake, licence, schema, review, split, evaluation, and reporting process. No language is excluded merely because it is not in the initial list; it is placed in a documented queue until evidence and data are available.

## 3. Definition of done for a language

A language track is complete when it has:

- at least 1,500 unique, reviewed bilingual sentence pairs, or an explicit documented exception;
- confirmed language variety, ISO code, and geographic provenance;
- source URL, edition/version, retrieval date, and licence metadata;
- source-specific raw and processed files;
- quality checks for duplicates, empty fields, language identity, alignment, and encoding;
- train/dev/test splits with no source or verse leakage;
- a reproducible model-evaluation record in both translation directions where possible;
- saved metric scores, model outputs, and error notes; and
- a language README describing limitations and review status.

## 4. Standard data model

All accepted bitext must use a common JSONL/CSV schema. Recommended fields are:

```json
{
  "language": "Mashi",
  "iso_code": "shr",
  "variety": "Mashi / Shi",
  "region": "South Kivu",
  "source": "source and edition name",
  "source_url": "https://example.org/source",
  "retrieved_at": "2026-08-21",
  "record_id": "stable-source-specific-id",
  "reference": "book/chapter/verse or source identifier",
  "source_text": "text in the Congolese language",
  "target_language": "French",
  "target_text": "aligned translation",
  "unit_type": "sentence",
  "domain": "biblical/news/education/etc.",
  "licence": "licence or permission reference",
  "review_status": "reviewed",
  "quality_flags": "",
  "notes": "optional review notes"
}
```

Keep raw source files separate from normalized, reviewed, and benchmark files. Never overwrite raw data during cleaning.

## 5. Common pipeline

Every language follows these stages:

1. **Discover:** inventory candidate sources and language identifiers.
2. **Verify:** confirm variety, provenance, access route, licence, and source edition.
3. **Acquire:** download or request the source while preserving retrieval metadata.
4. **Extract:** parse HTML, USFM, PDF, CSV, JSON, or other formats using a source-specific adapter.
5. **Align:** align translations using stable IDs where available; otherwise use an auditable alignment method.
6. **Normalize:** clean whitespace and encoding while preserving meaningful spelling and diacritics.
7. **Filter:** remove duplicates, empty records, wrong-language records, and clearly invalid alignments.
8. **Review:** conduct native-speaker or qualified linguistic review and quarantine uncertain rows.
9. **Split:** create leakage-safe train/dev/test or evaluation-only partitions by source and document.
10. **Evaluate:** run the same prompts, models, directions, metrics, and sampling rules.
11. **Report:** save scores, outputs, metadata, limitations, and a short language summary.

## 6. Phase plan

### Phase 0 — Reproducibility and tooling setup

- Define the common schema and directory conventions.
- Create a language registry containing names, ISO codes, varieties, regions, and status.
- Record Python and package versions in a requirements file or lock file.
- Explore [`africa-bitext-builder`](https://pypi.org/project/africa-bitext-builder/) in an isolated environment:
  - install the package without changing the main environment;
  - inspect its PyPI metadata, documentation, examples, and public source repository;
  - identify supported input formats, alignment methods, language handling, licences, and outputs;
  - run a small local smoke test on two known text files;
  - compare its output with the Mashi extraction workflow; and
  - document whether it is used for discovery, extraction, alignment, filtering, or not used.
- Do not treat package output as validated data without the project’s normal review and provenance checks.

**Exit criterion:** a short tooling note, a reproducible installation, and a decision on how the package fits the pipeline.

### Phase 1A — National-language benchmark

Work in this order: Lingala, Kikongo ya Leta, Ciluba, and Congo Swahili. The order may change if source access makes another track substantially more ready.

For each language:

1. identify the strongest open or permissioned bitext sources;
2. collect at least 1,500 candidate sentence pairs;
3. preserve source and licence metadata;
4. clean and deduplicate the pairs;
5. obtain native-speaker review;
6. freeze a reviewed evaluation set;
7. run model evaluation in both directions where possible; and
8. save the dataset card, scores, outputs, and error analysis.

**Exit criterion:** four national language tracks meeting the definition of done, or a documented shortfall with the reason and next data-collection action.

### Phase 1B — Regional top-five selection and collection

1. Build a regional candidate table.
2. Rank candidates using population/importance, representation gap, source availability, licensing, and review feasibility.
3. Select up to five feasible languages per region.
4. Create a worksheet and source inventory for each selected language.
5. Apply the common pipeline and 1,500-pair target.
6. Evaluate each completed language independently.

**Exit criterion:** a defensible top-five-per-region shortlist and the first completed regional language tracks with usable bitext.

### Phase 2 — Kivu expansion

1. Consolidate the existing Kivu language tracks and identify their remaining data gaps.
2. Add new Kivu languages from the regional candidate table where credible bitext exists.
3. Apply the common pipeline, native-speaker review, and evaluation protocol.
4. Compare Kivu results with the national and other regional tracks.

**Exit criterion:** an evaluated Kivu-focused expansion that clearly documents what was added to the existing Kivu coverage.

### Phase 3 — Continuous expansion

- Add newly discovered languages through the same intake form.
- Version datasets when sources or review decisions change.
- Maintain a backlog of contact leads and permission requests.
- Re-run evaluations when models, prompts, or benchmark versions change.
- Keep a changelog so results remain interpretable over time.

## 7. Evaluation protocol

For every language and direction, save:

- model name, version, and provider;
- prompt template and decoding settings;
- dataset version, split, source, and number of examples;
- predictions and references;
- BLEU and chrF++ scores, with tokenization settings;
- native-speaker quality assessment where available;
- representative successes and failures; and
- known limitations, including domain and source overlap.

Automatic metrics are comparisons, not complete judgments. Human review is required for final claims, especially for very small datasets and languages with spelling variation.

## 8. Repository layout

```text
language_resources/
  <language>-<iso>/
    README.md
    data/
      raw/
      processed/
      benchmark/
    metadata/
    scripts/
notebooks/
evaluations/
  <language>-<iso>/
    predictions/
    scores.json
    report.md
registry/
  languages.csv
  regional_candidates.csv
PROJECT_SPEC.md
```

The current repository may be migrated toward this layout incrementally. Existing Mashi files remain valid source artifacts while the shared schema is introduced.

## 9. Quality, ethics, and licensing rules

- Do not merge related languages or varieties without evidence and speaker validation.
- Keep native, human-translated, mined, machine-translated, and synthetic text labelled and separate.
- Do not scrape or redistribute a source merely because it is viewable online.
- Preserve attribution, licence, contributor, and edition metadata.
- Obtain community and contributor review where possible.
- Do not publish personal, sensitive, or restricted material without appropriate permission.
- Report missing data and uncertainty honestly; a small verified set is preferable to a large undocumented set.

## 10. Immediate next actions

1. Add the language registry and common schema.
2. Explore and smoke-test `africa-bitext-builder`.
3. Package the current Mashi workflow as the reference adapter.
4. Start the Lingala source inventory and target 1,500 reviewed pairs.
5. Repeat for Kikongo ya Leta, Ciluba, and Congo Swahili.
6. Create and rank the top-five-per-region candidate table while the national tracks are underway.
7. Collect and evaluate the selected regional languages with verified usable bitext.
8. Begin the dedicated Kivu expansion only after the national and broader regional tracks are complete.
