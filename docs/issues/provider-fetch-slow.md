# Requests to the external rainfall provider are slow / inconsistent

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py::test_report_shape`

## Problem description
The reporting endpoint sometimes fetches from a provider URL and
behaves inconsistently; local mock testing is hard.

## Expected behaviour
Provider fetch has clear timeout/error handling and a mock mode.

## Acceptance criteria
- [ ] Timeout and error paths covered by tests.
- [ ] Mock provider works on localhost.

## Reproduction steps
1. `GET /api/report?source=http://127.0.0.1:9000/provider` locally.
