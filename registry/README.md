# Language registry

`languages.csv` is the central tracker for language identity, project scope, pair targets, current status, and next actions.

`regional_candidates.csv` is the provisional top-five-per-region shortlist. Its `bitext_status` must be changed from `source_to_verify` only after a usable, permissioned or openly licensed bitext source has been confirmed.

Rules:

- Keep ISO codes and varieties explicit.
- Do not merge related varieties without linguistic or community validation.
- `current_pairs` counts only reviewed benchmark pairs, not raw candidates or catalogue records.
- Update `status` as a track moves through discovery, extraction, review, and evaluation.
- Add new languages as new rows rather than changing an existing language’s identity.
