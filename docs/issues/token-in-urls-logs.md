# Token appears in URLs and logs

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`, `frontend/app.js`
- **Relevant public test:** `tests/test_api.py`

## Problem description
Demo tokens appear in request URLs and server logs.

## Expected behaviour
Tokens travel in headers, expire, and are redacted from logs.

## Acceptance criteria
- [ ] No tokens in URLs or log output.
- [ ] Expired tokens are rejected.

## Reproduction steps
1. Inspect local logs and browser URLs.
