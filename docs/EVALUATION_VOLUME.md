# Evaluation volume

Generated from the frozen `v1` benchmark and prompt `translation_v1`.
These are exact record/character/whitespace-token counts, not model-tokenizer
counts. Input and generated token counts are captured during production.

- Language tracks: **47**
- Directions per track: **2**
- Requests per model: **141,000**
- Prompt characters per model: **36,897,141**
- Prompt whitespace tokens per model: **5,906,338**
- Five-model theoretical maximum: **705,000 requests**

The theoretical maximum assumes every model supports every track. Gemma,
Apertus, and BLOOMZ run 141,000 requests each; MADLAD and NLLB run smaller
matrices determined by exact model language-code coverage.

## Frozen pairs by reference language

| Reference language | Pairs |
|---|---:|
| English | 16,500 |
| French | 54,000 |

## Machine-readable summary

```json
{
  "language_tracks": 47,
  "directions": 2,
  "requests_per_model": 141000,
  "input_characters_per_model": 15732141,
  "input_whitespace_tokens_per_model": 2774338,
  "prompt_characters_per_model": 36897141,
  "prompt_whitespace_tokens_per_model": 5906338,
  "reference_language_frozen_pairs": {
    "English": 16500,
    "French": 54000
  }
}
```
