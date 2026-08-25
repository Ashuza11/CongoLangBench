# Official EPUB alignment

- Language: Kibembe (`bmb`), Democratic Republic of the Congo
- Parallel language: French
- Publication: *Enjoy Life Forever* (`lff`)
- Publisher/API: JW.org official publication media API
- Retrieved: 2026-08-25
- Kibembe EPUB: 102,193,080 bytes; MD5 `9532f19f01c6a1e83112ee7058b97319`
- French EPUB: 104,221,815 bytes; MD5 `b8740a391105ffde9c9373bcc997d19e`
- Licence: copyrighted; redistribution not authorized
- Repository handling: raw and processed text is Git-ignored and retained only
  for local research/evaluation

## Method

`download_publications.py` resolves the current official download URLs and
checks the publisher-provided MD5 hashes. `prepare_epub.py` reads only the main
publication XHTML documents, excludes bundled extracted-reference documents,
and joins French and Kibembe paragraphs using the shared document ID and
`data-pid`. Empty and duplicate pairs are removed.

## Result

- French paragraphs found: 3,252
- Kibembe paragraphs found: 3,255
- Unique aligned pairs: 2,984
- Empty source/target fields: 0
- Duplicate record IDs: 0
- Duplicate text pairs: 0
