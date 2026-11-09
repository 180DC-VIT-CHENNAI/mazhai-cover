# Issue #4 — Incorrect single-hour trigger (Medium)
# Bug: Single-hour rainfall incorrectly triggers a two-hour policy

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/triggers.py` (`detect_events`)
- **Relevant public test:** `tests/test_triggers.py::test_single_hour_must_not_trigger_two_hour_policy`

## Problem description
Any single hour >= 20 mm fires immediately (`streak >= 1`), so a
one-hour spike triggers a policy requiring two consecutive hours.
It also emits two events for one 2-hour spell.

## Expected behaviour
Events require `consecutive_hours` (2) consecutive rainy hours.

## Acceptance criteria
- [ ] Isolated 1-hour spike yields zero events.
- [ ] A 2-hour spell yields exactly one event (correct start/end).
- [ ] Below-threshold runs still yield zero.

## Reproduction steps
1. `pytest tests/test_triggers.py::test_single_hour_must_not_trigger_two_hour_policy -v`
