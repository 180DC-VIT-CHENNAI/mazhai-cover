# Dashboard loses rider preferences unpredictably

- **Difficulty:** Easy
- **Affected file:** `frontend/app.js`
- **Relevant public test:** `tests/test_frontend.py`

## Problem description
Rider preference objects sometimes carry unexpected leftover keys after merges across drafts.

## Expected behaviour
Preferences merge safely with a known schema.

## Acceptance criteria
- [ ] Merged preferences contain only expected keys.
- [ ] Frontend tests cover the merge.

## Reproduction steps
1. Merge a local JSON draft in the browser console.
