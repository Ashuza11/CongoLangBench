# Google SMOL Ciluba acquisition

- Dataset: [Google SMOL](https://huggingface.co/datasets/google/smol)
- Language: Tshiluba / Ciluba (`lua`)
- Licence: CC BY 4.0
- Retrieval date: 2026-08-21
- Files acquired: `gatitos/lua_en.jsonl` and `gatitos/en_lua.jsonl`
- File sizes: 2,708 and 3,998 rows respectively

These are GATITOS lexical translations, not sentence-level bitext. No `SmolSent/en_lua.jsonl`, `SmolSent/lua_en.jsonl`, `SmolDoc/en_lua.jsonl`, or `SmolDoc/lua_en.jsonl` file was available in the current SMOL release. The lexicon is preserved as supporting data and does **not** count toward the 1,500-sentence national benchmark target.

The package registry exposes Ciluba Bible versions, but those editions require source-specific licence verification before extraction. The next acquisition route is therefore the gated `multi-open` Tshiluba resource, a permissioned Bible alignment, or a separate community/publisher-provided sentence corpus.

## multi-open access status (2026-08-21)

The accepted `english-tshiluba` configuration exposes `data/english-tshiluba/train-00000.parquet` and reports approximately 400,000 English--Tshiluba rows. The local download attempt returned HTTP 401 because the local Hugging Face token has not inherited the browser approval. Authenticate locally, download that exact file, then run `scripts/prepare_multi_open.py`. The script preserves `translation_quality_score` as an automatic Gemma-judge field; it is not human gold data.

## Sentence-level leads

- [African Languages Lab `multi-open`](https://huggingface.co/datasets/African-Languages-Lab/multi-open) reports a large English-target collection including Tshiluba, but files require sharing contact information and accepting dataset conditions. Its licence is listed as `other`; do not download, count, or redistribute rows until the terms are reviewed.
- The African Languages Lab’s broader text/speech work includes Tshiluba, but the public speech/text catalogue is not automatically a downloadable bilingual sentence corpus. Treat it as a contact lead until item-level access and licence are confirmed.
- The SMOL GATITOS files remain useful lexical support only; they do not satisfy the 1,500-sentence requirement.
