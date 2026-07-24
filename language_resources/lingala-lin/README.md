# Lingala (`lin`)

Search names/codes: Lingala, `lin`, `ln`, `lin_Latn`. “Ngala” is ambiguous and requires ISO verification.

## Verified and evaluated data

| DATA | Resource | Access/licence | Evaluation |
|---|---|---|---|
| **BITEXT + LEXICON** | [Google SMOL](https://huggingface.co/datasets/google/smol): `gatitos__en_ln`, `smolsent__en_ln`, `smoldoc__en_ln` | **OPEN**, CC BY 4.0 | Professionally translated English–Lingala lexical, sentence, and document data. Keep components separate. |
| **BITEXT** | [WMT22 African](https://huggingface.co/datasets/allenai/wmt22_african); [paper](https://aclanthology.org/2022.wmt-1.72/) | **OPEN**, ODC-By 1.0 | Automatically mined Common Crawl/ParaCrawl. Training-scale but noisy; audit language ID, alignment, toxicity, and duplicates. |
| **BITEXT** | [AfriNLLB-train](https://huggingface.co/datasets/AfriNLP/AfriNLLB-train) | **NONCOMMERCIAL**, CC BY-NC 4.0 | Includes Lingala pairs from multiple sources. Preserve source provenance; not unrestricted commercial data. |
| **BITEXT** | [multi-open](https://huggingface.co/datasets/African-Languages-Lab/multi-open) | **GATED**, licence “other” | Card reports about 390,000 English–Lingala rows. Gating and unspecified terms mean it is not open. |
| **BITEXT (evaluation)** | [FLORES](https://github.com/facebookresearch/flores), `lin_Latn` | repository terms | Small human-translated `dev`/`devtest`; evaluation, not a large training corpus. |
| **SPEECH + TEXT** | [BibleTTS](https://masakhane-io.github.io/bibleTTS/); [paper](https://arxiv.org/abs/2207.03546) | inspect current release | Studio Lingala scripture speech aligned with text. Religious/read-speech domain; verify file licence before redistribution. |
| **LEXICON** | [dic.lingala.be](https://dic.lingala.be/en/) | **TERMS / permission** | Real Lingala–French/English entries and examples; no bulk open-data licence verified. Contact `dic@lingala.be`. |

## Best sources you can use now

1. **DATA — FULL BIBLE TEXT — OPEN (CC BY-SA 4.0):** [Biblica Open Lingala Contemporary Bible](https://preview.open.bible/bibles/lingala-biblica-text-bible) provides direct **USFM, USX, and Word** downloads. This is the strongest immediately downloadable Lingala text source. Its page identifies the DRC and states CC BY-SA.
2. **DATA — PARALLEL BIBLE:** align the Lingala USFM verse IDs with an equivalently licensed French or English Bible from the [Open.Bible catalog](https://www.open.bible/bibles). Keep the Lingala and translation licences/attribution files with the aligned output.
3. **DATA — DICTIONARY:** [dic.lingala.be](https://dic.lingala.be/en/) gives Lingala headwords with French/English definitions and examples. It is usable for manual research now; request a licensed bulk export for corpus creation.
4. **DATA — DIRECT PDF:** [download the Lingala Bible PDF](https://downloads.open.bible/text/ln/lnOMNB20/lnOMNB20_PDF.pdf) when USFM is not needed.

## Convertible and monolingual sources

- **DATA — BIBLE — MIXED:** [eBible Corpus](https://github.com/BibleNLP/ebible) and [JHU Bible Corpus](https://github.com/christos-c/bible-corpus). A verse-indexed edition is monolingual until legally compatible translations are aligned.
- **DATA — MONOLINGUAL — MIXED:** Lingala Wikipedia and web-crawl datasets exist. Inspect origin, licence, deduplication, and MT/synthetic fields.
- **DATA — LEXICON — OPEN:** [ASJP](https://asjp.clld.org/) and Wiktionary/Kaikki may supply small wordlists; confirm exact entries and attribution.

## Quarantined findings

- [Central Africa Multilingual Translation](https://huggingface.co/datasets/Svngoku/central-africa-multilingual-translation) claims millions of pairs but has inadequate provenance and no clear licence: **UNVERIFIED / DO NOT INGEST**.
- [Congolese-languages speech](https://huggingface.co/datasets/Svngoku/speech-recognition-congolese-languages) does not substantiate its advertised total and lacks a clear licence: contact lead only.
- Synthetic programming/dialogue and sentiment uploads are not native corpora. Exclude from native-data totals.
- `kurukanpublishing/lingua-patria` does not currently provide a populated Lingala column according to its card.

## Related work, searches, and contacts

- [MMTAfrica](https://aclanthology.org/2021.wmt-1.48/) · [AfroMT](https://aclanthology.org/2021.emnlp-main.99/) · [LiSTra](https://aclanthology.org/2022.dclrl-1.8/)
- [ACL](https://aclanthology.org/search/?q=Lingala) · [arXiv](https://arxiv.org/search/?query=Lingala&searchtype=all) · [Hugging Face](https://huggingface.co/datasets?search=Lingala) · [GitHub](https://github.com/search?q=Lingala+dataset&type=repositories)

Contact BibleTTS/Masakhane, WMT22 authors, `dic.lingala.be`, and Lingala publishers, broadcasters, translators, and university language/CS departments. No dedicated Lingala LDC Babel, TED, or OpenSubtitles release was verified.
