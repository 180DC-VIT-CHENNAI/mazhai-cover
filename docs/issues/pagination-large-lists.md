# Frontend breaks when API returns large zone lists

- **Difficulty:** Easy
- **Affected file:** `frontend/app.js`
- **Relevant public test:** `tests/test_frontend.py`

## Problem description
Large zone lists stall the dashboard rendering.

## Expected behaviour
Large lists paginate or render lazily.

## Acceptance criteria
- [ ] Dashboard handles 100+ zones without stalling.
- [ ] Pagination or virtual list present.

## Reproduction steps
1. Seed a local fixture with many zones; load UI.
