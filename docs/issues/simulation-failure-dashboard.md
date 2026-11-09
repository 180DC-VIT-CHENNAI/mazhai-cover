# When simulation fails, the whole dashboard fails

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py`

## Problem description
A simulation error makes report/webhook responses fail entirely.

## Expected behaviour
Simulation failures degrade to partial results with a clear error state.

## Acceptance criteria
- [ ] Report works when simulation is faulted (mocked locally).
- [ ] Dashboard shows partial data + error note.

## Reproduction steps
1. Fault the simulation locally; load `/api/report`.
