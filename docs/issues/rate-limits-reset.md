# Rate limits are easy to reset

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py`

## Problem description
Changing a header resets per-client request counting.

## Expected behaviour
Limits are tied to a stable client identity that cannot be spoofed by headers alone.

## Acceptance criteria
- [ ] Changing header values does not reset limits.
- [ ] Limits apply to demo traffic locally.

## Reproduction steps
1. Rotate header values locally and watch counting.
