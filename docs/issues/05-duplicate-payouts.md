# Issue #5 — Duplicate payouts for the same event (Medium)

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/payouts.py` (`deduplicate_events`)
- **Relevant public test:** `tests/test_payouts.py::test_duplicate_events_collapse_to_one`

## Problem description
`deduplicate_events` returns its input untouched, so the same
zone+spell emitted twice (e.g. overlapping windows) pays out multiple
Rs.500 payouts.

## Expected behaviour
One payout per unique (zone_id, start_time, end_time) event.

## Acceptance criteria
- [ ] Identical duplicates collapse to one.
- [ ] Distinct spells/zones are preserved.
- [ ] Stable ordering after dedup.

## Reproduction steps
1. `pytest tests/test_payouts.py::test_duplicate_events_collapse_to_one -v`
