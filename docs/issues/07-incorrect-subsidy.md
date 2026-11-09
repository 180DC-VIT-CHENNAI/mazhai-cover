# Issue #7 — Incorrect subsidy calculation (Easy)

- **Difficulty:** Easy
- **Affected file:** `src/mazhai/payouts.py` (`calculate_subsidy`)
- **Relevant public test:** `tests/test_payouts.py::test_subsidy_only_for_eligible_riders`

## Problem description
The eligibility flag is inverted: non-eligible riders receive
Rs.50/month while eligible riders receive nothing.

## Expected behaviour
Subsidy only when `subsidy_eligible` is true.

## Acceptance criteria
- [ ] Eligible → Rs.50; non-eligible → Rs.0.
- [ ] `premium_with_subsidy` keeps working (never negative).

## Reproduction steps
1. `pytest tests/test_payouts.py::test_subsidy_only_for_eligible_riders -v`
