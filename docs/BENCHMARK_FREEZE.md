# Benchmark freeze

Benchmark version **v1** freezes exactly **1,500** evaluation
pairs for each of **47** ready language tracks, for a total of
**70,500** evaluation pairs.

The selection is deterministic: records are ranked by
`sha256(congolang-bitext-eval-v1\0iso\0record_id), lowest 1500`. Every frozen set is evaluation-only; no training split is
created, so benchmark verses or sentences cannot leak into a project training
partition. Source overlap with external model pretraining remains a documented
limitation, especially for religious-domain datasets.

All benchmark text is currently Git-ignored. Open-source tracks can be
regenerated from tracked processed data; restricted tracks are reproducible
from their local authorized source workflow. The tracked manifest records
source and frozen-output checksums without redistributing restricted text.

## Summary

- Frozen language tracks: **47**
- Evaluation pairs per track: **1,500**
- Total evaluation pairs: **70,500**
- Restricted local tracks: **24**

## Tracks by registry group

- Central DRC: 4
- DRC-wide: 4
- Ituri: 5
- Kivu: 7
- Maniema: 5
- Northern DRC: 5
- Northwestern Congo Basin: 5
- Southeastern DRC: 5
- Tshopo: 3
- Western DRC: 4

## Reproduction

```bash
venv/bin/python -u scripts/audit_curation_readiness.py
venv/bin/python -u scripts/freeze_benchmarks.py
```

See `registry/benchmark_freeze.csv` for per-language source and benchmark
checksums.
