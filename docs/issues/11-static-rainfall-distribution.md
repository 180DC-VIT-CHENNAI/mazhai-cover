# Issue #11 — Static rainfall distribution (Hard)
# Feature: Extreme rainfall trends are ignored

- **Difficulty:** Hard
- **Affected file:** `src/mazhai/simulation.py` (`run_monte_carlo`)
- **Relevant public test:** smoke test via `python -m mazhai.main`

## Problem description
The simulator uses a fixed mean every year. Extreme-rainfall frequency
is rising (climate trend), so a static model underprices future risk.

## Expected behaviour
Add a trend/extreme-rainfall parameter (e.g. mean grows x% per year or
tail probability rises) with the projection documented.

## Acceptance criteria
- [ ] Trend parameter exists and defaults to documented, sane values.
- [ ] Later simulated years show higher tail payouts than earlier years.
- [ ] Backwards compatible; docstring updated.

## Reproduction steps
1. Inspect `run_monte_carlo` — no trend term is present.
