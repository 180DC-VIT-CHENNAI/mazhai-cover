# Cache goes stale after zone data changes

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py::test_report_shape`

## Problem description
Pricing/report cache stays stale after editing `zones.csv`.

## Expected behaviour
Data changes are reflected without manual restart (or via explicit reload).

## Acceptance criteria
- [ ] Editing local CSV is reflected on next report.
- [ ] Reload path documented.

## Reproduction steps
1. Edit `data/zones.csv` locally; re-query `/api/report`.
