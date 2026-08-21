# Google SMOL Ciluba acquisition

- Dataset: [Google SMOL](https://huggingface.co/datasets/google/smol)
- Language: Tshiluba / Ciluba (`lua`)
- Licence: CC BY 4.0
- Retrieval date: 2026-08-21
- Files acquired: `gatitos/lua_en.jsonl` and `gatitos/en_lua.jsonl`
- File sizes: 2,708 and 3,998 rows respectively

These are GATITOS lexical translations, not sentence-level bitext. No `SmolSent/en_lua.jsonl`, `SmolSent/lua_en.jsonl`, `SmolDoc/en_lua.jsonl`, or `SmolDoc/lua_en.jsonl` file was available in the current SMOL release. The lexicon is preserved as supporting data and does **not** count toward the 1,500-sentence national benchmark target.

The package registry exposes Ciluba Bible versions, but those editions require source-specific licence verification before extraction. The next acquisition route is therefore the gated `multi-open` Tshiluba resource, a permissioned Bible alignment, or a separate community/publisher-provided sentence corpus.
