# Ngombe (`ngc`)

## Northwestern DRC track

The package exposes three public-domain Ngombe editions labelled for DRC/CAR:
Miwera, Bodjenga, and Bondjale. Each is aligned by canonical verse key with the
public-domain French Louis Segond 1910 edition. The project retains all
**12,735 unique aligned pairs** across the three editions rather than
truncating the track to 1,500 rows.

The editions are kept explicit in row metadata because their texts can differ.
Unicode and whitespace normalization plus exact-pair deduplication are the only
text transformations.

- [Source and alignment metadata](metadata/package_alignment.md)
- [Preparation script](scripts/prepare_package.py)
- [Africa Corpus catalogue](https://huggingface.co/datasets/AfriSpeech/africa-corpus)
