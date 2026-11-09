# The application slows down on large rainfall datasets

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`, `src/mazhai/data_loader.py`
- **Relevant public test:** `tests/test_api.py::test_report_shape`

## Problem description
`/api/report` re-reads large CSVs on every call and slows down as rows grow.

## Expected behaviour
Reports stay fast with a sensible caching strategy and stay correct after data changes.

## Acceptance criteria
- [ ] Repeat reports are served from cache.
- [ ] Changing local CSV data is reflected (no stale reports).

## Reproduction steps
1. Time repeated `/api/report` calls locally.
