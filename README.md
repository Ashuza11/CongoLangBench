# CongoLangBitextEval: Congolese Language Text Evaluation

[![Project Status](https://img.shields.io/badge/status-active_development-brightgreen)](#project-goal)
[![Task](https://img.shields.io/badge/task-bitext_evaluation-6f42c1)](#project-goal)
[![Language Coverage](https://img.shields.io/badge/coverage-13_language_tracks-007ec6)](#group-1--the-four-national-languages)
[![Data](https://img.shields.io/badge/data-bitext_%7C_lexicons_%7C_corpora-f39c12)](#evidence-labels)
[![Provenance](https://img.shields.io/badge/provenance-evidence_audited-2ea44f)](#collection-rules)
[![Licensing](https://img.shields.io/badge/licensing-source_specific-e05d44)](#evidence-labels)

CongoLangBitextEval is a text-evaluation initiative that curates high-quality datasets for all available Congolese languages and evaluates how state-of-the-art language models perform on them. Its primary focus is bilingual text (bitext) and machine translation, supported by monolingual corpora and bilingual lexicons where available. The project gives careful attention to language identity, provenance, licensing, and data quality.

## Project goal

The goal of this project is to build an inclusive, reproducible text-evaluation benchmark for Congolese languages by:

1. discovering and documenting available text resources for national, regional, and under-resourced Congolese languages;
2. collecting, cleaning, aligning, and validating monolingual text, parallel text, and bilingual lexicons where reuse is permitted;
3. preserving metadata about language variety, geographic origin, source, licence, and translation method;
4. creating carefully reviewed evaluation sets that avoid source overlap and train–test contamination; and
5. evaluating state-of-the-art language models on bilingual text and related language tasks to identify capabilities, performance gaps, and priorities for future data collection.

The current repository contains evidence-audited, copy-ready data-collection worksheets and an initial Mashi–French extraction and evaluation workflow. Resource inventory last checked: **2026-07-20**.

## Group 1 — The four national languages

| Constitutional name | Data-collection target | ISO 639-3 | Worksheet |
|---|---|---:|---|
| Lingala | Lingala | `lin` | [Lingala](language_resources/lingala-lin/README.md) |
| Ciluba | Ciluba / Tshiluba / Luba-Kasai | `lua` | [Ciluba](language_resources/ciluba-lua/README.md) |
| Kikongo | **Kikongo ya Leta / DRC Kituba** | `ktu` | [Kikongo ya Leta](language_resources/kituba-ktu/README.md) |
| Swahili | **Congo Swahili from the DRC only** | `swc` | [Congo Swahili](language_resources/congo-swahili-swc/README.md) |

The Constitution names “Kikongo,” but the national lingua franca commonly meant in present-day DRC is Kikongo ya Leta (DRC Kituba, `ktu`). The Kongo macrolanguage code `kon`, Koongo `kng`, and Angolan San Salvador Kongo `kwy` are not interchangeable with `ktu`.

The Swahili worksheet excludes generic/standard Swahili (`swa`, `swh`, `sw`). “Kingwana” is retained as a search term for northern/Ituri varieties, not as a synonym for every `swc` resource.

## Group 2 — Eastern DRC regional languages

These are languages, not collectively “dialects.”

| Language | ISO 639-3 | Core area | Worksheet |
|---|---:|---|---|
| Mashi / Shi | `shr` | Bukavu hinterland; Walungu, Kabare, Kalehe | [Mashi](language_resources/mashi-shr/README.md) |
| Nande / Kinande | `nnb` | Beni and Lubero; also neighboring areas | [Nande](language_resources/nande-nnb/README.md) |
| Hunde / Kihunde | `hke` | Masisi, Rutshuru, Walikale and nearby areas | [Hunde](language_resources/hunde-hke/README.md) |
| Fuliiru / Kifuliiru | `flr` | Uvira Plain and Uvira Territory | [Fuliiru](language_resources/fuliiru-flr/README.md) |
| Tembo / Kitembo | `tbt` | Kalehe, Masisi and Walikale | [Tembo](language_resources/tembo-tbt/README.md) |
| Havu / Kihavu | `hav` | Idjwi and Kalehe | [Havu](language_resources/havu-hav/README.md) |
| Nyanga / Kinyanga | `nyj` | Walikale | [Nyanga](language_resources/nyanga-nyj/README.md) |
| Lega-Mwenga | `leg` | Mwenga | [Lega](language_resources/rega-leg/README.md) |
| Lega-Shabunda | `lea` | Shabunda and Pangi | [Lega](language_resources/rega-leg/README.md) |

## Evidence labels

- **VERIFIED DATASET**: files, language identity, access route, and licence checked.
- **CONVERTIBLE SOURCE**: real content exists, but alignment, extraction, or permission is needed.
- **CATALOG RECORD**: proves a resource exists; it is not itself a corpus.
- **CONTACT LEAD**: plausible holder or creator, not confirmed data.
- **UNVERIFIED / DO NOT INGEST**: provenance, identity, size, or licence is insufficient.

Every data-bearing entry states type (**BITEXT**, **LEXICON**, **MONOLINGUAL**, **SPEECH**), access (**OPEN**, **GATED**, **TERMS**, **CLOSED**), licence, and quality caveats. “Free to read,” “downloadable,” and “available in an app” do not mean open-data reuse. A Bible becomes bitext only after verse alignment with a legally compatible translation.

## Best concrete source found for each language

| Language | Most actionable source now |
|---|---|
| Lingala | [Open.Bible full Bible](https://preview.open.bible/bibles/lingala-biblica-text-bible): direct USFM/USX/Word, CC BY-SA 4.0 |
| Tshiluba | [TSHILUBA.co](https://tshiluba.co/wordindex.html): about 800 web-indexed trilingual entries; [SMOL](https://huggingface.co/datasets/google/smol) adds an open English lexicon |
| Kikongo ya Leta | [SMOL](https://huggingface.co/datasets/google/smol): downloadable English–`ktu` lexicon, sentences, and documents, CC BY 4.0 |
| Congo Swahili | [CLEAR Global](https://mozilladatacollective.com/datasets/cmosl07v400w9nu07g3puif2t): downloadable French–`swc` TSV, 25,305 pairs, CC BY 4.0 |
| Mashi | [eBible Mashi](https://ebible.org/find/details.php?id=shr): full Bible/developer formats, CC BY 4.0; plus a [Mashi–Hebrew–French contextual dictionary](https://nyabangere.com/wp-content/uploads/2025/08/deuteronome-dictionnaire-contextuel-mashi-hebreu-francais.pdf) |
| Nande | [ASJP wordlist](https://asjp.clld.org/languages/J42_NANDE), CC BY 4.0; larger Kinande–French dictionary requires library/rightsholder contact |
| Hunde | [Kihunde Living Dictionary](https://livingdictionaries.app/kihunde): multilingual entries and audio; request export/permission |
| Fuliiru | [Kifuliiru Dictionary](https://dictionary.kifuliiru.net/dictionary): Kifuliiru–Swahili–English–French plus audio; request export/permission |
| Tembo | [YouVersion Tembo](https://www.bible.com/languages/tbt) plus [Glosbe Tembo–French](https://fr.glosbe.com/tbt/fr); permission required for bulk extraction |
| Havu | [eBible Havu New Testament](https://ebible.org/hav/index.htm): downloadable formats, CC BY-SA 4.0 |
| Nyanga | [Kinyanga audio app](https://play.google.com/store/apps/details?id=com.kinyanga.goma.rdc): Kinyanga–French/Swahili verse display and synchronized audio; permission required for extraction |
| Lega-Shabunda | [Kilega Bible record/app](https://find.bible/bibles/LEAUFM/): full Bible with parallel French/Swahili app; permission required |
| Lega-Mwenga | No concrete bulk text/lexicon verified; community and publisher outreach is required |

## General resources and cautions

- [Google SMOL](https://huggingface.co/datasets/google/smol): professionally translated multilingual lexical, sentence, and document resources, CC BY 4.0. Confirm which component exists per language.
- [FLORES](https://github.com/facebookresearch/flores): small human-translated **evaluation** sets, not training-scale corpora.
- [eBible Corpus](https://github.com/BibleNLP/ebible): verse-indexed translations with edition-specific licences.
- [JHU Bible Corpus](https://github.com/christos-c/bible-corpus): aligned religious text; retain source-edition provenance and rights metadata.
- [OPUS](https://opus.nlpl.eu/) and [MTData](https://github.com/thammegowda/mtdata): indexes/downloaders with corpus-specific licences and quality.
- **JW300:** **historical lead only**. [OPUS](https://opus.nlpl.eu/) withdrew the corpus download after rights concerns; do not cite an obsolete corpus URL as available data.
- [Hugging Face](https://huggingface.co/datasets), [GitHub](https://github.com/search), [ACL Anthology](https://aclanthology.org/), and [arXiv](https://arxiv.org/) are discovery platforms, not quality or licence guarantees.
- [ASJP](https://asjp.clld.org/): small standardized wordlists, CC BY 4.0; useful for lexical comparison, not sentence MT.
- [PanLex](https://panlex.org/), [Wiktionary dumps](https://dumps.wikimedia.org/), and [Kaikki](https://kaikki.org/): confirm actual exact-language coverage before claiming data.
- [OSCAR](https://oscar-project.github.io/documentation/), [CC-100](https://data.statmt.org/cc-100/), and [Wikipedia dumps](https://dumps.wikimedia.org/): validate automatic language identification for closely related Bantu varieties.

## Collection rules

1. Preserve URL, retrieval date, ISO code, regional variety, edition, licence, and attribution.
2. Never merge `ktu`, `kon`, `kng`, or `kwy` merely because a page says “Kikongo.”
3. Never merge `leg` and `lea` without community/linguist validation.
4. For Congo Swahili, require explicit DRC provenance; generic Swahili is outside scope.
5. Keep native, human-translated, mined, machine-translated, and LLM-generated data separate.
6. Deduplicate Bible verses and overlapping releases before reporting totals.
