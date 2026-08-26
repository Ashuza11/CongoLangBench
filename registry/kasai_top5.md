# Kasai / Central DRC top five

Selection is based on regional relevance **and confirmed usable open bitext**.
The completed national Tshiluba track represents the region without being
duplicated as a second resource.

| Rank | Language | ISO | Open bitext | Status |
|---:|---|---|---:|---|
| 1 | Tshiluba / Luba-Kasai | `lua` | 397,971 processed pairs | Reuse completed national track |
| 2 | Tetela | `tll` | 222,212 processed pairs | Curated |
| 3 | Songe / Kisonge | `sop` | 51,069 processed pairs | Curated |
| 4 | Ruund / Uruund | `rnd` | 133,626 processed pairs | Curated DRC-labelled track |
| 5 | Kanyok / Kanyoka | `kny` | 4,788 restricted local pairs | Curated for local evaluation |

All five tracks are now curated. The active set is restricted to languages and
source varieties from the DRC.
Kanyok replaces the Angola-labelled Chokwe source. Kanyok is a substantial
Kasai--Lomami language with approximately 582,000 DRC speakers in one current
population-oriented estimate. Its six-book official jw.org source yielded
4,808 verses and 4,788 unique French--Kanyok pairs for local evaluation. The
text remains Git-ignored because it is not openly licensed for redistribution.

I also checked two open alternatives for the fifth Kasai slot:

- Kete / Kikete (`kcv`) is available only as Mark and Luke portions on
  YouVersion/Bible.com, which currently yields 1,438 aligned pairs — below the
  1,500-pair minimum.
- Kuba / Luna (`luj`) resolves to a single Luke source on YouVersion/Bible.com
  in the current extraction path, so it also falls below the threshold.

Those alternatives remain documented, but Kanyok completes the fifth Kasai
slot.

The already curated Angola-labelled Chokwe dataset is retained only in the
regional backlog as a documented cross-border comparison source; it is not one
of the Kasai top five. Luba-Lulua and Kuba/Bushoong remain important acquisition
candidates. Luba-Lulua must not be silently presented as a separate language
track when the available source uses the same `lua` identity as Tshiluba.
