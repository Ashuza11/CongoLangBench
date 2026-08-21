# Ciluba / Tshiluba / Luba-Kasai (`lua`)

## Project files

- [Raw SMOL lexicon](data/raw/)
- [SMOL metadata](metadata/smol.md)

Do not mix `lua` with Luba-Katanga (`lub`) or results about the Lua programming language.

## Verified and evaluated data

| DATA | Resource | Access/licence | Evaluation |
|---|---|---|---|
| **LEXICON** | [Google SMOL](https://huggingface.co/datasets/google/smol), `gatitos__en_lua` | **OPEN**, CC BY 4.0 | About 4,000 professionally translated English–Tshiluba GATITOS entries. Mainly lexical; no `smolsent__en_lua` or `smoldoc__en_lua` was verified. |
| **BITEXT (evaluation)** | [FLORES](https://github.com/facebookresearch/flores), `lua_Latn` | repository terms | Small human-translated evaluation set, not training-scale. |
| **BITEXT** | [multi-open](https://huggingface.co/datasets/African-Languages-Lab/multi-open) | **GATED**, licence “other” | Accepted by project owner; local token still needs access. Card reports about 400,000 English–Tshiluba rows. |
| **LEXICON** | [TSHILUBA.co](https://tshiluba.co/) | **TERMS / permission** | Searchable Tshiluba–French–English dictionary; request export instead of scraping. |

## Convertible sources and leads

- **DATA — BIBLE — MIXED:** [eBible Corpus](https://github.com/BibleNLP/ebible), [JHU Bible Corpus](https://github.com/christos-c/bible-corpus), [Scripture Earth](https://www.scriptureearth.org/), and [find.bible](https://find.bible/). Align exact, legally compatible editions only.
- The [NLLB Tshiluba–English model card](https://huggingface.co/SalomonMetre13/nllb-lua-en-mt-v1) says scraped Bible pairs were used but does not publish a documented source corpus. **MODEL/CONTACT LEAD**, not dataset.
- [Multilingual Sentiment Lexicon](https://arxiv.org/abs/2411.04316) mentions Tshiluba. Confirm a separate download and licence before marking DATA.
- Wikipedia/web-crawl results need `lua` language-ID validation against neighboring Luba varieties.

## Best sources you can use now

1. **DATA — ONLINE TRILINGUAL DICTIONARY:** [TSHILUBA.co word index](https://tshiluba.co/wordindex.html) exposes about **800 indexed Tshiluba headword pages** with French and English fields/examples. It is immediately useful for manual lookup or a permission-based lexicon export.
2. **DATA — GATED SENTENCE DOWNLOAD:** [multi-open](https://huggingface.co/datasets/African-Languages-Lab/multi-open), configuration `english-tshiluba`, supplies about 400,000 rows after local authentication. Run `scripts/prepare_multi_open.py` after placing the Parquet file in `data/raw/`.
3. **DATA — OPEN LEXICON DOWNLOAD:** [Google SMOL](https://huggingface.co/datasets/google/smol), configuration `gatitos__en_lua`, supplies about 4,000 English–Tshiluba lexical items under CC BY 4.0.
3. **DATA — SCRIPTURE TEXT LEAD:** [YouVersion Tshiluba search](https://www.bible.com/search/bible?q=Tshiluba) and [Scripture Earth](https://www.scriptureearth.org/) can identify exact editions. App/web access is usable for inspection; contact the publisher for bulk USFM or redistribution rights.
4. **CONTACT:** ask TSHILUBA.co (`info@tshiluba.co`) for CSV/JSON/database export and explicit research/redistribution terms. This is preferable to scraping hundreds of pages.

## Searches and contacts

- [ACL Tshiluba](https://aclanthology.org/search/?q=Tshiluba) · [ACL Ciluba](https://aclanthology.org/search/?q=Ciluba)
- [arXiv](https://arxiv.org/search/?query=Tshiluba&searchtype=all) · [Hugging Face](https://huggingface.co/datasets?search=Tshiluba) · [GitHub](https://github.com/search?q=Tshiluba+dataset&type=repositories)
- [Scholar machine translation](https://scholar.google.com/scholar?q=%22Tshiluba%22+%22machine+translation%22)

Contact Google SMOL, `multi-open`, the NLLB model uploader, TSHILUBA.co (`info@tshiluba.co`), and Tshiluba linguists, publishers, broadcasters, translators, and faculty in Kasai. No verified dedicated LDC/Babel, OPUS, TED, or OpenSubtitles package was found.
