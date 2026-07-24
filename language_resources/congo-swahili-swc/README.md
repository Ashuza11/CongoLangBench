# Congo Swahili (`swc`) — DRC-only track

Include only data explicitly tied to DRC Swahili. Generic Standard Swahili (`swa`, `swh`, `sw`) is excluded. Search Congo/Congolese/Zaïre Swahili and regional names (Kivu, Katanga, Maniema, Ituri). “Kingwana” is especially associated with northern/Ituri usage and is not a safe synonym for all `swc`.

## Verified and evaluated data

| DATA | Resource | Access/licence | Evaluation |
|---|---|---|---|
| **BITEXT** | [CLEAR Global/Gamayun French–Congo Swahili kits](https://mozilladatacollective.com/datasets/cmosl07v400w9nu07g3puif2t) | **OPEN**, CC BY 4.0 | 25,305 TSV pairs in three kits (5,000; 10,000; 10,305). Human translation; deduplicate and inspect variety/domain. |
| **BITEXT inventory** | [Congolese Swahili MT for Humanitarian Response](https://arxiv.org/abs/2103.10734) | component-specific | AfricaNLP 2021, not EAMT. Reports TWBkits, TICO-19, TWBinTM, and historical JW300 inputs. Paper counts do not prove current availability/rights. |
| **SPEECH TRANSLATION / catalog** | [IWSLT 2021 task](https://iwslt.org/2021/low-resource); [overview](https://aclanthology.org/2021.iwslt-1.1/) | registration/terms | Explicit Congolese Swahili task. Treat as a catalog record until current files and terms are obtained. |

## Corrections and exclusions

- OPUS JW300 was withdrawn after rights concerns; see the current [OPUS catalog](https://opus.nlpl.eu/). Older experimental counts are **not a currently open download**.
- Bible/YouVersion/Scripture Earth text is not automatically open or bitext.
- Tatoeba may contain `swc`, but verify current count, attribution, and download licence before claiming a corpus.
- [Congolese-languages speech](https://huggingface.co/datasets/Svngoku/speech-recognition-congolese-languages) does not substantiate its claimed total and lacks a clear licence: **UNVERIFIED / DO NOT INGEST**.
- Exclude CC100, OSCAR, Wikipedia, TED, OpenSubtitles, FLEURS, or any corpus labeled only generic Swahili.

## Best sources you can use now

1. **DATA — DOWNLOADABLE BITEXT — OPEN (CC BY 4.0):** [CLEAR Global French–Congo Swahili kits](https://mozilladatacollective.com/datasets/cmosl07v400w9nu07g3puif2t). Click **Download**; each TSV includes raw `swc`, cleaned `swc_clean`, and French. This is the first source to acquire.
2. **DATA — ONLINE DICTIONARY/TRANSLATION MEMORY:** [Glosbe Congo Swahili–French](https://glosbe.com/swc/fr) exposes `swc` headwords and translated sentence examples. Useful for manual inspection; Glosbe display access is not permission to bulk-copy its translation memory.
3. **DATA — TATOEBA LEAD:** search/download sentences tagged Congo Swahili from [Tatoeba downloads](https://tatoeba.org/en/downloads). Retain sentence IDs and attribution and confirm current licence/quality. Native review is essential because community language labels may be inconsistent.
4. **DATA — HISTORICAL DICTIONARY LEADS:** [Lexilogos Swahili dictionary bibliography](https://www.lexilogos.com/swahili_dictionnaire.htm) links colonial Congo vocabularies. Include only entries whose locality/variety is demonstrably Congolese; most generic Swahili works remain out of scope.

## Searches and contacts

- [ACL](https://aclanthology.org/search/?q=%22Congo%20Swahili%22) · [arXiv](https://arxiv.org/search/?query=%22Congolese+Swahili%22&searchtype=all) · [Hugging Face](https://huggingface.co/datasets?search=swc) · [GitHub](https://github.com/search?q=%22Congolese+Swahili%22+dataset&type=repositories)
- [Scholar Kingwana](https://scholar.google.com/scholar?q=Kingwana+translation)

Contact CLEAR Global/Gamayun, credited translators, AfricaNLP/IWSLT authors, DRC humanitarian translators, radio/newsrooms, and language departments. Start with the 25,305 CC BY pairs, preserve kit IDs, deduplicate, and obtain regional native-speaker review.
