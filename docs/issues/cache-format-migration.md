# Pricing cache format needs a migration path

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py`

## Problem description
The local pricing cache uses a dense binary-ish format that is brittle across restarts and version changes.

## Expected behaviour
Cache format is inspectable, versioned, and migrates cleanly.

## Acceptance criteria
- [ ] Cache payload is human-inspectable JSON.
- [ ] Invalid/old payloads are rejected with a clear error.

## Reproduction steps
1. Save cache, restart, restore; inspect payload.
