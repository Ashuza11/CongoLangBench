# Mashi / Shi (`shr`)

Mashi is part of the current Eastern regional top five. Its clean benchmark
track now contains **1,500 verified-source Mashi--French pairs**, selected
deterministically from 30,911 open aligned candidates. See the
[curation metadata](metadata/eastern1500.md) and
[preparation script](scripts/prepare_eastern1500.py).

Search Mashi, Shi, Kishi, Cishi, Bashi, Bushi, `shr`; “Shi” alone is noisy.

## Verified data

- **DATA — MONOLINGUAL / CONVERTIBLE BITEXT — OPEN (CC BY 4.0):** [BIBLIYA NTAGATIFU OMU MASHI](https://ebible.org/find/details.php?id=shr), complete 2024 Bible with Deuterocanon. Developer downloads include USFM, USFX, VPL/SQL, plain text, HTML, and EPUB. Align verse IDs to a compatibly licensed translation; the Mashi file alone is not bitext.
- **DATA — LEXICON — OPEN (CC BY 4.0):** [ASJP Mashi DRC](https://asjp.clld.org/languages/MASHI_DRC), a small standardized concept wordlist. Useful for lexical comparison, not sentence MT.

## Leads, searches, and evaluation

- [Scripture Earth `shr`](https://www.scriptureearth.org/00i-Scripture_Index.php?iso=shr) catalogs text, audio, and film. It is a discovery page; item-level rights apply.
- Bible.is/Faith Comes By Hearing audio is a **SPEECH CONTACT LEAD**, not open training data unless its licence says so.
- Descriptive grammars and theses may contain examples/wordlists but are copyrighted publications; obtain permission before bulk extraction.
- **DATA — TRILINGUAL CONTEXT DICTIONARY PDF:** [*Deutéronome: dictionnaire contextuel mashi–hébreu–français*](https://nyabangere.com/wp-content/uploads/2025/08/deuteronome-dictionnaire-contextuel-mashi-hebreu-francais.pdf) derives Mashi forms from the open eBible edition and supplies French contextual equivalents. The PDF is directly readable/downloadable; its own reuse licence is not stated in the search record, so request permission before bulk redistribution.
- [ACL](https://aclanthology.org/search/?q=%22Mashi%22) · [arXiv](https://arxiv.org/search/?query=%22Mashi%22+language&searchtype=all) · [Hugging Face](https://huggingface.co/datasets?search=Mashi) · [GitHub](https://github.com/search?q=Mashi+language+dataset&type=repositories) · [Scholar](https://scholar.google.com/scholar?q=%22Mashi%22+%22machine+translation%22)

No verified `shr` package was found in LDC/Babel, OPUS, OSCAR, CC100, FLORES, TED, OpenSubtitles, or a standalone Wikipedia. Contact the named eBible contributor, Mashi linguists in Bukavu/Walungu/Kabare/Kalehe, publishers, broadcasters, churches, and university language/CS departments.

## Best workflow now

1. Download the [Mashi eBible developer formats](https://ebible.org/find/details.php?id=shr) under CC BY 4.0.
2. Align its book/chapter/verse identifiers with a compatible French or English Bible.
3. Use the contextual dictionary PDF as terminology/reference data, while asking its author/site for an extractable table and licence.
4. Use the [ASJP Mashi wordlist](https://asjp.clld.org/languages/MASHI_DRC) as a small independent spelling/lexical cross-check.
