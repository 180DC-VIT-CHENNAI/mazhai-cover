# Zone-level reports become inconsistent under concurrent updates

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py` (webhooks / report)
- **Relevant public test:** `tests/test_api.py`

## Problem description
Parallel payout/report requests sometimes show totals that do not
match the weekly cap or prior reads.

## Expected behaviour
Concurrent updates converge to consistent totals.

## Acceptance criteria
- [ ] Parallel local requests give consistent totals.
- [ ] No lost updates under load in local tests.

## Reproduction steps
1. Fire parallel local webhook POSTs; compare with fresh report.
