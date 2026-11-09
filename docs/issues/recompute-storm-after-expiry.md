# Several clients trigger recomputation at once after cache expiry

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py` (`/api/simulate`)
- **Relevant public test:** `tests/test_api.py::test_simulate_returns_portfolio`

## Problem description
After the simulation cache expires, many concurrent requests each recompute.

## Expected behaviour
Only one recomputation runs; others wait for or reuse the result.

## Acceptance criteria
- [ ] Concurrent simulate calls trigger one computation.
- [ ] Results are shared with waiters.

## Reproduction steps
1. Fire concurrent local simulate calls after TTL.
