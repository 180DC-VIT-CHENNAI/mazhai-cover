# Difficult to trace a request end-to-end

- **Difficulty:** Easy
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py`

## Problem description
Logs lack shared identifiers, so following one request through the app is guesswork.

## Expected behaviour
Each request carries a consistent identifier across logs and responses.

## Acceptance criteria
- [ ] Logs include a request identifier.
- [ ] Response carries the same identifier.

## Reproduction steps
1. Send two local requests; try to correlate logs.
