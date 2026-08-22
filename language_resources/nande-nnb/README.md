# Nande / Kinande (`nnb`)

## Curation status

The public track contains **14,949 unique French--Nande sentence pairs** from
CLEAR Global's independent 5,000- and 10,000-sentence Gamayun kits. All usable
rows are retained and published under CC BY 4.0 with CLEAR Global attribution.
See the [Gamayun metadata](metadata/gamayun_kits.md) and reproducible
[preparation script](scripts/prepare_gamayun.py).

The earlier 1,500-pair Bible sample generated through `africa-bitext-builder`
remains local-only because its Nande edition is marked non-public-domain. It is
documented as a supplementary restricted source, not part of the public track.

Search Nande, Kinande, Kinandi, Yira, Luyira, Orundande, `nnb`. The core DRC concentration is Beni and Lubero; “North Kivu, Ituri” should not imply equal distribution.

## Verified data and catalogs

- **DATA — LEXICON — OPEN (CC BY 4.0):** [ASJP J42 Nande](https://asjp.clld.org/languages/J42_NANDE), a downloadable standardized concept wordlist with ISO `nnb`. Small lexicon, not sentence bitext.
- **CATALOG RECORD — BIBLE — TERMS:** [find.bible Nande](https://find.bible/languages/nnb/) identifies Kinande/Kinandi scripture. A catalog/app listing does not establish bulk access or an open licence; contact the named publisher.
- **CONVERTIBLE SOURCE — BIBLE — MIXED:** search [eBible Corpus](https://github.com/BibleNLP/ebible), [Scripture Earth](https://www.scriptureearth.org/), and [JHU Bible Corpus](https://github.com/christos-c/bible-corpus) by `nnb` and edition. Confirm exact text and rights before alignment.

## Corrections, searches, and contacts

- **DATA — PARALLEL TEXT — OPEN (CC BY 4.0):** [CLEAR Global Gamayun French--Nande kits](https://huggingface.co/datasets/CLEAR-Global/Gamayun-kits) provide 15,000 raw general-domain rows across independent 5k and 10k kits. The repository publishes all 14,949 unique normalized pairs.
- Generic PanLex/Wiktionary statements are leads until a specific `nnb` entry/export is confirmed.
- **DATA — BILINGUAL DICTIONARY BOOK:** P. Guibert Baudet, [*Éléments de grammaire kinande; suivis d’un vocabulaire kinande–français et français–kinande*](https://catalogue.bnf.fr/ark:/12148/cb37017107x). The BnF record confirms both directions; it is a library/digitization lead, not a downloadable open corpus.
- **DATA — SMALL WIKTIONARY:** [French Wiktionary Kinande category](https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:kinande) currently has only a small number of entries. Wiktionary content is downloadable under its open licence, but coverage is tiny.
- [ACL](https://aclanthology.org/search/?q=Kinande) · [arXiv](https://arxiv.org/search/?query=Kinande&searchtype=all) · [Hugging Face](https://huggingface.co/datasets?search=Kinande) · [GitHub](https://github.com/search?q=Kinande+dataset&type=repositories) · [Scholar](https://scholar.google.com/scholar?q=%22Kinande%22+%22machine+translation%22)

No verified `nnb` LDC/Babel, OPUS, OSCAR, CC100, FLORES, TED, OpenSubtitles, or Wikipedia corpus was found. Contact CLEAR Global for historical kit status, the Bible publisher, Kinande linguists/educators in Beni and Butembo, Radio Moto, Yira organizations, and local university language/CS departments.

## Best workflow now

1. Use the complete public Gamayun track as the primary benchmark source.
2. Use the CC BY 4.0 [ASJP Nande wordlist](https://asjp.clld.org/languages/J42_NANDE) for lexical cross-checking.
3. Locate the Baudet Kinande–French/French–Kinande volume through BnF/library loan and contact the publisher/rightsholder for OCR/reuse permission.
4. Ask the publisher listed by [find.bible](https://find.bible/languages/nnb/) for verse-keyed USFM plus an explicit research licence.
