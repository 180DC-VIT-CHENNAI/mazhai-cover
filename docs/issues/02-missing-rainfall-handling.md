# Issue #2 — Missing rainfall handling (Easy)
# Bug: Missing observations are treated as zero

- **Difficulty:** Easy
- **Affected file:** `src/mazhai/data_loader.py` (`parse_rainfall_row`)
- **Relevant public test:** `tests/test_data_loader.py::test_missing_rainfall_is_none_not_zero`

## Problem description
Empty `rainfall_mm` cells are coerced to 0.0 (dry hour) instead of
`None` (unknown), so gaps look like confirmed dry weather and break
consecutive-hour counting silently.

## Expected behaviour
Missing → `rainfall_mm is None`; explicit "0.0" → 0.0 (dry).

## Acceptance criteria
- [ ] Missing cells surface as `None`.
- [ ] Explicit 0.0 is still a valid dry hour.
- [ ] Trigger counting treats `None` as unknown/not-rainy (no crash).

## Reproduction steps
1. `pytest tests/test_data_loader.py::test_missing_rainfall_is_none_not_zero -v`
