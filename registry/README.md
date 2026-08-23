# Language registry

`languages.csv` is the central tracker for language identity, project scope, pair targets, current status, and next actions.

`regional_candidates.csv` is the provisional top-five-per-region shortlist. Its `bitext_status` must be changed from `source_to_verify` only after a usable, permissioned or openly licensed bitext source has been confirmed.

`national_sources.csv` and `national_sources.md` track the Phase 1A source verification plan for the four national languages.

`eastern_top5.md` records the selected Eastern DRC top-five bitext tracks and
separates them from the later dedicated Kivu expansion.

`katanga_top5.md` records the completed bitext-feasible Southeastern DRC set
and explains why Sanga remains in the acquisition backlog.

`kasai_top5.md` records the bitext-feasible Kasai/Central DRC set. The national
Tshiluba resource is reused rather than duplicated as a regional dataset.

Rules:

- Keep ISO codes and varieties explicit.
- Do not merge related varieties without linguistic or community validation.
- `current_pairs` counts normalized usable pairs from accepted sources, not raw catalogue records.
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

The Southeastern DRC/Katanga track is complete. Kiluba has 197,411
open English pairs from MT560, and Tabwa has 5,039 open French pairs aligned
from the CC BY-SA 4.0 Kitaabua edition. Bemba replaces Sanga in the current
top five because it has usable open bitext; Sanga remains identity-verified in
the acquisition backlog. Aushi now has 1,900 open cross-border
pairs from Zambian editions and exceeds the project minimum.
Lunda now has a complete open MT560 track with 134,568 normalized candidates,
also labelled as cross-border rather than DRC-specific.

The Kasai/Central DRC track is now in progress. Its feasible top five are
Tshiluba, Tetela, Songe, Chokwe, and Ruund. Tshiluba reuses the completed
national track. Tetela is the first newly curated regional resource, with
222,212 normalized English--Tetela pairs from a DRC-labelled CC BY 4.0 source.
Songe now has 51,069 normalized DRC-labelled English pairs. The active top five
are restricted to DRC languages and varieties: Tshiluba, Tetela, Songe, Ruund,
and Kanyok. Ruund now has 133,626 normalized DRC-labelled English pairs. Kanyok
has a documented complete DRC Bible whose digital text and reuse terms must be obtained. The curated
Angola-labelled Chokwe source is retained only in the regional backlog.
