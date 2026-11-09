# Admin pages reachable from a public deployment

- **Difficulty:** Medium
- **Affected file:** `frontend/app.js`, `src/mazhai/api.py`, README deployment notes
- **Relevant public test:** `tests/test_api.py`

## Problem description
Behind a CDN/reverse proxy, admin-ish pages and direct backend addresses are reachable from the public frontend.

## Expected behaviour
Deployment notes describe how to keep admin/direct access closed; public frontend does not expose direct backend addresses.

## Acceptance criteria
- [ ] Deployment notes cover proxy + admin access.
- [ ] Public frontend does not hardcode a direct backend host.

## Reproduction steps
1. Compare direct vs proxied local runs; inspect JS config.
