# Evaluation model selection

Status: **proposed, not yet run**

Matrix version: `v1`

Selection date: 2026-08-26

The first benchmark comparison uses three hosted model families and one
open-weight baseline. This gives a useful capability/cost/reproducibility
comparison without treating a single provider as representative of all modern
models.

| Track | Exact model identifier | Purpose |
|---|---|---|
| Hosted frontier | `gpt-5.6-sol` | OpenAI's current flagship Sol variant, avoiding the routing alias `gpt-5.6` |
| Hosted cost-efficient | `gemini-3.7-flash` | A stable Google production model suitable for a large matrix |
| Hosted frontier balanced | `claude-sonnet-5` | A pinned Anthropic release with strong multilingual capability |
| Open-weight local | `google/gemma-4-12B` | A reproducible baseline that can run outside a hosted API |

The machine-readable settings are in
`evaluations/model_matrix.json`. The matrix intentionally does not use
`latest` aliases. Model access, exact API response metadata, token usage, and
run date must still be captured when inference is executed.

## Fair-comparison configuration

- Use prompt `translation_v1` for every model and language.
- Run both directions for all 47 tracks: reference-to-Congolese and
  Congolese-to-reference.
- Use all 1,500 frozen examples for final results.
- Disable sampling or thinking where the provider supports that control.
- Do not force a universal `temperature=0`: current Claude Sonnet 5 and Gemini
  APIs reject custom sampling fields. Omit those fields and record the
  provider-specific behavior.
- Limit output to 512 tokens and retain only the translation text for scoring.
- Save retries, refusals, empty outputs, token counts, latency, and provider
  request IDs. Never replace a failed request with a different model.

## Execution order

1. Run a 10-example smoke test on Lingala (`lin`), Congo Swahili (`swc`), and
   Hunde (`hke`) in both directions.
2. Check output-only compliance, encoding, retries, and scoring coverage.
3. Estimate hosted cost from actual smoke-test token usage.
4. Obtain explicit approval for credentials and budget.
5. Run the full 47-language matrix, one model at a time.
6. Score BLEU and chrF++, then add structured error analysis and speaker review
   before making quality claims.

No paid API request is authorized merely by selecting this matrix.

## Primary references

- OpenAI current model comparison and GPT-5.6 guidance:
  <https://developers.openai.com/api/docs/models/compare> and
  <https://developers.openai.com/api/docs/guides/latest-model>
- Google Gemini model and pricing documentation:
  <https://ai.google.dev/gemini-api/docs/models> and
  <https://ai.google.dev/gemini-api/docs/pricing>
- Anthropic model identifiers and model overview:
  <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions>
  and <https://platform.claude.com/docs/en/about-claude/models/overview>
- Gemma 4 model card:
  <https://huggingface.co/google/gemma-4-12B>
