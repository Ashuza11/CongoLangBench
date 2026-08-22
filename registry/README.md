# Language registry

`languages.csv` is the central tracker for language identity, project scope, pair targets, current status, and next actions.

`regional_candidates.csv` is the provisional top-five-per-region shortlist. Its `bitext_status` must be changed from `source_to_verify` only after a usable, permissioned or openly licensed bitext source has been confirmed.

`national_sources.csv` and `national_sources.md` track the Phase 1A source verification plan for the four national languages.

Rules:

- Keep ISO codes and varieties explicit.
- Do not merge related varieties without linguistic or community validation.
- `current_pairs` counts only reviewed benchmark pairs, not raw candidates or catalogue records.
- Update `status` as a track moves through discovery, extraction, review, and evaluation.
- Add new languages as new rows rather than changing an existing language’s identity.

## Regional phase entry

The first regional track is South Kivu. Mashi currently has 1,168 curated
French–Mashi candidates, so it remains below the 1,500-pair target. Its next
action is to add a compatible, permissioned or openly licensed source. Nande
(`nnb`) now has 14,949 public French--Nande pairs from CLEAR Global. Havu now
has 3,224 public Havu--French verse pairs. Fuliiru, Tembo, and Nyanga follow as
sources are verified.
