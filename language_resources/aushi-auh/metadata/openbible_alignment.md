# Aushi--French alignment

- Aushi source: [Aushi Bible Translation Project](https://preview.open.bible/bibles/aushi-bible-translation-project)
- Provider: The Word for the World International
- Source country label: Zambia
- Aushi licence: CC BY-SA 4.0
- French source: Louis Segond 1910, public domain
- Extraction adapter: `africa-bitext-builder` 0.1.13
- Package version IDs: Aushi `4447`, French `93`
- Retrieval date: 2026-08-22
- Package-aligned rows: 1,226
- Bible in Every Language Mark units: 674
- Unique processed pairs: 1,900
- Raw SHA-256: `c3be315f4edeed5b23c83dc8bacf9283b8a707b2e8bc618ee31b3266cc34fdf8`
- Aushi Mark PDF SHA-256: `7f7b761a35adb8c9417e672497ad3f55c1cc45f72ff079379c0579e753e7c001`
- French reference CSV SHA-256: `02bda5a1696b4848967f64fa535a67c9a88ff8bd166900bf9d2780fdc1dc6008`
- Coverage: Matthew (1,071), Mark (674), James (108), 2 Thessalonians (47)
- Margin above 1,500: 400

Open.Bible describes the item as a full Bible, but its official USFM download
on the retrieval date contains only the same three books exposed through the
package. The project records the downloadable coverage rather than the page's
broader label.

The supplemental [Aushi Mark PDF](https://doc-files.bibleineverylanguage.org/auh-reg-mrk_lbo_1c_c_chapter_clf.pdf)
is ©2022 Wycliffe Associates and explicitly released under CC BY-SA 4.0. Its
678 verse references become 674 aligned units because the source combines four
pairs of adjacent references. The PDF
text is aligned with the public-domain French Segond version 93 by canonical
reference. PDF page furniture is removed; wording is otherwise preserved.

Aushi is spoken across Zambia and southeastern DRC. These rows are valid open
Aushi data, but their source provenance is Zambian. Every processed row carries
the `cross_border_variety` quality flag so later evaluation does not silently
treat it as a DRC-specific edition.
