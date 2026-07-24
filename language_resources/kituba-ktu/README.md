# Kikongo ya Leta / DRC Kituba (`ktu`)

This worksheet implements the DRC national-language track. [ScriptSource](https://www.scriptsource.org/cms/scripts/page.php?item_id=subtag_detail&uid=xalnwf4cny) and [Glottolog](https://glottolog.org/resource/languoid/id/kitu1246) identify DRC Kituba as `ktu`, with Kikongo ya Leta among its names. Republic-of-the-Congo Kituba/Monokutuba (`mkw`), the Kongo macrolanguage (`kon`), Koongo (`kng`), and San Salvador Kongo (`kwy`) must remain separate.

## Verified and evaluated data

- **DATA — VERIFIED DATASET — BITEXT/LEXICON — OPEN (CC BY 4.0):** [Google SMOL](https://huggingface.co/datasets/google/smol), configurations `gatitos__en_ktu`, `smolsent__en_ktu`, and `smoldoc__en_ktu`. Professionally translated English–DRC Kituba. GATITOS is mainly lexical; SmolSent and SmolDoc contain parallel sentences/documents.
- **DATA — CONVERTIBLE SOURCE — BIBLE — MIXED LICENCES:** search [eBible Corpus](https://github.com/BibleNLP/ebible), [Scripture Earth](https://www.scriptureearth.org/), and [find.bible](https://find.bible/) for `ktu` and edition names. Record the exact licence before alignment.
- **DATA — LEXICON — OPEN:** [ASJP](https://asjp.clld.org/) provides small standardized wordlists; retain exact source/variety metadata.

## Rejected or quarantined claims

- [English–“Kikongo” MT560](https://huggingface.co/datasets/michsethowusu/english-kikongo_sentence-pairs_mt560) is `kwy` (San Salvador Kongo/Angola), not `ktu`.
- FLORES `kon_Latn` is labeled with the Kongo macrolanguage, not verified DRC Kituba.
- [Central Africa Multilingual Translation](https://huggingface.co/datasets/Svngoku/central-africa-multilingual-translation) has no clear reusable licence and insufficient variety/provenance documentation: **UNVERIFIED / DO NOT INGEST**.
- Wikipedia-derived “Kikongo” and synthetic dialogue uploads often mix `kg`, `kon`, and Kituba labels. Require native-speaker language ID and a source/licence audit.

## Best sources you can use now

1. **DATA — OPEN BITEXT/LEXICON:** [Google SMOL](https://huggingface.co/datasets/google/smol) configurations `gatitos__en_ktu`, `smolsent__en_ktu`, and `smoldoc__en_ktu` are the cleanest downloadable English–DRC Kituba resources.
2. **DATA — DICTIONARY BOOK / DIGITIZATION LEAD:** Harold W. Fehderau, [*Dictionnaire kikongo (ya leta)–anglais–français*](https://books.google.com/books/about/Dictionnaire_kikongo_ya_leta_anglais_fra.html?id=qkoHAQAAIAAJ), 323 pages (1969). Google Books confirms the exact target variety and three languages but offers no ebook. Locate a library copy and secure digitization/reuse permission.
3. **DATA — BIBLE TEXT:** [WorldBibles Kituba index](https://worldbibles.org/language_detail/fra/ktu/Kikongo-Kutuba) identifies Kituba editions. [JW.org’s `ktu` Bible page](https://www.jw.org/ktu-x-kgl/bibloteke/biblia/) provides readable/downloadable `ktu` text/PDF/audio, but JW terms do not grant corpus/training reuse; use for inspection and contact the rightsholder.
4. **DATA — PUBLIC-DOMAIN LEAD:** the 1894 *Vocabulaire pratique français–anglais–zanzibarite–swahili–fiote* is useful only if the “fiote” variety is verified as relevant; do not relabel it `ktu` without linguistic review.

## Searches and contacts

- [ACL Kituba](https://aclanthology.org/search/?q=Kituba)
- [arXiv Kituba](https://arxiv.org/search/?query=Kituba&searchtype=all)
- [Hugging Face Kituba](https://huggingface.co/datasets?search=Kituba)
- [GitHub Kituba dataset](https://github.com/search?q=Kituba+dataset&type=repositories)
- [Scholar “Kikongo ya Leta” MT](https://scholar.google.com/scholar?q=%22Kikongo+ya+Leta%22+%22machine+translation%22)

Contact Google SMOL maintainers/translators and DRC Kituba linguists, broadcasters, publishers, Bible translators, and CS/linguistics faculty in Kongo Central and Kinshasa. No verified target-specific LDC/Babel, OPUS, OSCAR, CC100, OpenSubtitles, TED, or standalone Wikipedia package was found.
