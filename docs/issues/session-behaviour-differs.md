# Session behaviour differs between dev and prod-like setups

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py`
- **Relevant public test:** `tests/test_api.py`

## Problem description
Session/cookie settings differ between local runs, so contributors
see inconsistent sign-in or preference persistence across setups.

## Expected behaviour
Session settings are explicit per environment and the same locally.

## Acceptance criteria
- [ ] Settings documented and set explicitly.
- [ ] Local and proxied local setups behave the same.

## Reproduction steps
1. Compare responses on localhost vs proxied localhost.
