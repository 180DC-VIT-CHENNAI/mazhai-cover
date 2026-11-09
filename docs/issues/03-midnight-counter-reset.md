# Issue #3 — Consecutive-hour counter resets at midnight (Medium)
# Bug: Rainfall trigger incorrectly resets at midnight

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/triggers.py` (`detect_events`)
- **Relevant public test:** `tests/test_triggers.py::test_midnight_crossing_counts_as_consecutive`

## Problem description
The consecutive counter resets when the calendar date changes, so an
uninterrupted 23:00 + 00:00 spell never accumulates to a 2-hour trigger.

## Expected behaviour
If rainfall exceeds threshold at 11 PM and midnight (next day),
a two-hour trigger activates spanning the boundary.

## Acceptance criteria
- [ ] Consecutive rainfall tracked across calendar boundaries.
- [ ] Ordinary same-day behaviour unchanged.
- [ ] Regression test covers midnight-crossing events.

## Reproduction steps
1. `pytest tests/test_triggers.py::test_midnight_crossing_counts_as_consecutive -v`
2. Note the event ends at 23:00 instead of 00:00 next day.
