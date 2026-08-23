# Pende open-source inventory

## Language identity

- Language: Pende / Phende
- ISO 639-3: `pem`
- Country: Democratic Republic of the Congo
- Project region: Western DRC (Kwango--Kwilu)
- Required alignment: French--Pende or English--Pende
- Minimum target: 1,500 sentence pairs

## Open non-religious corpora checked

Status checked: 2026-08-23.

| Collection | Coverage check | Result |
| --- | --- | --- |
| OPUS | Official API queries for `pem`--`fr` and `pem`--`en` | Zero corpora returned |
| MaLA bilingual translation corpus | Exact repository paths for `pem_Latn` paired with `fra_Latn` or `eng_Latn`, in both directions | No matching pair exists |
| African Languages Lab `multi-open` | Published list of 31 English--African-language configurations | Pende is not included |
| GlotLID corpus | `pem_Latn` is represented | Monolingual language-identification material, not bitext |
| ASJP | Pende language material is represented | Word-list data, not sentence bitext |

Generic multilingual collections must not be counted as coverage unless their
language inventory contains ISO `pem` and the actual aligned files are
accessible under usable terms. Search-result mentions alone are insufficient.

## Other leads

Find.Bible catalogues Pende editions, including the 1996 `PEMFUL` edition and a
2025 New Testament. These are fallback leads only: catalogue presence does not
establish an open licence for extracting and redistributing a sentence dataset.
No text from them is included here.

## Acquisition routes

1. Request existing translation memories from DRC education, health,
   humanitarian, localization, and community-language organizations.
2. Locate bilingual readers, public-information documents, dictionaries with
   full translated examples, or subtitled media carrying explicit open terms.
3. Accept a community-contributed corpus only with source provenance, language
   variety, alignment method, and a redistribution licence.
4. If only restricted data becomes available, keep its text outside Git and
   publish metadata, scripts, aggregate statistics, and permitted results only.

An acquired source must contain real human-authored or source-authenticated
Pende text. Machine-translated synthetic Pende must be tracked separately and
must not be presented as the primary curated benchmark.

## Reference links

- OPUS API: https://opus.nlpl.eu/opusapi/
- MaLA corpus: https://huggingface.co/datasets/MaLA-LM/mala-bilingual-translation-corpus
- African Languages Lab multi-open: https://huggingface.co/datasets/African-Languages-Lab/multi-open
- GlotLID corpus: https://huggingface.co/datasets/cis-lmu/glotlid-corpus
- ASJP: https://asjp.clld.org/

