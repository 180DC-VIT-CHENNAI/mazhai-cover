# Filters with long inputs hang the server

- **Difficulty:** Easy
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py::test_report_zone_filter`

## Problem description
Very long zone filter values in `/api/report?zone=` can take a long time to answer.

## Expected behaviour
Inputs are bounded and validated quickly; long values rejected fast.

## Acceptance criteria
- [ ] Long inputs return promptly with a clear error.
- [ ] Normal zone filters still work.

## Reproduction steps
1. Request `/api/report?zone=` with a long local string.
