# Reporting endpoint behaves inconsistently behind a reverse proxy

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py::test_report_shape`

## Problem description
Report responses differ when the app runs directly vs behind a
reverse proxy. Client/host handling is inconsistent.

## Expected behaviour
Same inputs give the same report regardless of proxy setup; host
handling is explicit and documented.

## Acceptance criteria
- [ ] Report stable through a local proxy mock.
- [ ] Host handling documented in README deployment notes.

## Reproduction steps
1. Run directly and via local proxy; compare `/api/report`.
