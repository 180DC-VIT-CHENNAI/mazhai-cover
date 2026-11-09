# Issue #6 — Weekly payout cap ignored (Medium)

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/payouts.py` (`apply_weekly_cap`)
- **Relevant public test:** `tests/test_payouts.py::test_weekly_cap_enforced`

## Problem description
`apply_weekly_cap` returns all events regardless of the zone's
`weekly_payout_cap` (see `zones.csv`), so heavy weeks pay far beyond
the product cap.

## Expected behaviour
At most `weekly_cap // payout_amount` payouts pass through.

## Acceptance criteria
- [ ] Total payouts after cap <= weekly cap.
- [ ] Highest-priority (earliest) events kept first.
- [ ] Caps below one payout yield zero.

## Reproduction steps
1. `pytest tests/test_payouts.py::test_weekly_cap_enforced -v`
