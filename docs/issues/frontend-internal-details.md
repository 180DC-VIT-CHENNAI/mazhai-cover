# Frontend shows internal details in network calls

- **Difficulty:** Medium
- **Affected file:** `frontend/app.js`
- **Relevant public test:** `tests/test_frontend.py`

## Problem description
The public JS bundle and network tab show internal API paths/endpoints
that should only be visible to maintainers.

## Expected behaviour
Public frontend only holds public endpoints; internal paths are not shipped to browsers.

## Acceptance criteria
- [ ] Built JS contains only public endpoint paths.
- [ ] Dashboard still loads reports.

## Reproduction steps
1. Open Network tab on a local run.
