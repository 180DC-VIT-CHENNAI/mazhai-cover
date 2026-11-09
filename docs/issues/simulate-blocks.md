# Simulate endpoint blocks while running long jobs

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py::test_simulate_returns_portfolio`

## Problem description
`/api/simulate` runs synchronously and blocks the server during computation.

## Expected behaviour
Dashboard stays responsive; simulation can run asynchronously or return cached results.

## Acceptance criteria
- [ ] Other endpoints respond during simulation.
- [ ] Cached simulate results are reused.

## Reproduction steps
1. Call `/api/simulate` while polling `/api/health`.
