# OR CrossLedger

Conservative reconciliation of payments from two ledgers with explicit ambiguity instead of forced matching.

## Why it matters

Reconciliation errors can hide operational breaks or create false investigative links. This project matches only when amount, currency, time, references, and supplied account fields agree. Competing candidates remain visible for review.

## Current capabilities

- Canonical decimal, currency, timestamp, and identifier validation.
- Reference-based or unique amount/currency/time matching.
- Optional source and destination account agreement.
- Permutation-invariant results and explicit ambiguous/unmatched queues.
- Metrics and review flags for weaker matches.
- CLI, optional authenticated API, Docker image, and CI.

## Run

```sh
python -m pip install -e '.[dev,api]'
python -m or_crossledger --demo
pytest -q && ruff check src tests
```

API: set `OR_API_KEY` to at least 16 characters, run `uvicorn or_crossledger.api:create_app --factory`, then POST `examples/request.json` to `/v1/analyze`.

## Limitations and roadmap

This is not a settlement engine and does not infer a match from approximate text or FX conversion. It has no ISO 20022 adapters, fee handling, split/merge reconciliation, reversals, durable exception queue, or accounting controls. Next steps are typed source adapters, provenance per normalized field, configurable tolerances by rail, reconciliation aging, and reviewed-match feedback.
