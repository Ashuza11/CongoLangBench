# Language registry

`languages.csv` is the central tracker for language identity, project scope, pair targets, current status, and next actions.

`regional_candidates.csv` is the provisional top-five-per-region shortlist. Its `bitext_status` must be changed from `source_to_verify` only after a usable, permissioned or openly licensed bitext source has been confirmed.

`national_sources.csv` and `national_sources.md` track the Phase 1A source verification plan for the four national languages.

`eastern_top5.md` records the selected Eastern DRC top-five bitext tracks and
separates them from the later dedicated Kivu expansion.

Rules:

- Keep ISO codes and varieties explicit.
- Do not merge related varieties without linguistic or community validation.
- `current_pairs` counts only reviewed benchmark pairs, not raw candidates or catalogue records.
- Update `status` as a track moves through discovery, extraction, review, and evaluation.
- Add new languages as new rows rather than changing an existing language’s identity.

## Regional phase entry

The first regional track is Eastern DRC. Mashi now has a clean 1,500-pair
French--Mashi benchmark selected from 30,911 open aligned candidates. Nande
(`nnb`) has 14,949 public French--Nande pairs from CLEAR Global. Havu
has 3,224 public pairs reserved for the later Kivu expansion. Fuliiru has 30,546 technically
aligned pairs but remains permission-required. Tembo has 7,932 technically
aligned New Testament pairs and is also permission-required. Nyanga has 3,192
technically aligned pairs with a licence conflict that must be resolved.

The Southeastern DRC/Katanga track is now in progress. Kiluba has 197,411
open English pairs from MT560, and Tabwa has 5,039 open French pairs aligned
from the CC BY-SA 4.0 Kitaabua edition. Sanga is identity-verified but requires
digital source access and redistribution permission. Aushi and Lunda remain
the next two source-discovery targets. Aushi now has 1,226 open cross-border
pairs from a Zambian edition and needs 274 more, preferably with DRC provenance.
Lunda now has a complete open MT560 track with 134,568 normalized candidates,
also labelled as cross-border rather than DRC-specific.
