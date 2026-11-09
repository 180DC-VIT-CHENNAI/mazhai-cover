# One heavy zone slows all other zones

- **Difficulty:** Hard
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py::test_report_shape`

## Problem description
Traffic for one zone degrades reports for all other zones.

## Expected behaviour
Zones are isolated so one heavy zone does not affect the rest.

## Acceptance criteria
- [ ] Heavy-zone load does not slow other-zone reports substantially.
- [ ] Per-zone metrics exist in local logs.

## Reproduction steps
1. Load one zone heavily locally; time other zones.
