# Contributing to Mazhai Cover

Thanks for picking up a Mazhai Cover issue! This is a small, friendly
starter repo — the goal is correct financial logic and clean PRs, not
heroics.

## Workflow

1. **Find an issue** in `docs/issues/` (or GitHub Issues) — start with Easy
   (#1, #2, #7) if you're new.
2. **Create a branch**: `fix/issue-<N>-<short-slug>`, e.g.
   `fix/issue-3-midnight-counter`.
3. **Reproduce**: write or run the relevant public test and confirm it fails
   for the seeded bug:
   ```bash
   pytest tests/test_triggers.py -v
   ```
4. **Fix** in the module named by the issue. Keep public function
   signatures stable — other modules and tests depend on them.
5. **Test locally**: `pytest -q` and `python -m mazhai.main`.
6. **Open a PR** referencing the issue (`Closes #3`). Describe what you
   changed and how you verified it.

## Ground Rules

- One issue per branch/PR where possible.
- Don't add dependencies without discussion — numpy + stdlib is enough.
- Don't commit generated data changes unless the issue needs them.
- Keep the pricing report printing — `python -m mazhai.main` must still run.

## Tests

Public tests in `tests/` mirror the issues: failing tests are your spec.
If you fix a bug, the matching test should go green without breaking the
passing ones. Add a regression test for tricky fixes (e.g. midnight
crossing, duplicate events).

## Simulation Contributions (#10, #11)

`simulation.py` documents its assumptions. Improvements should:

- Keep `run_monte_carlo(zones, ...)` signature-compatible.
- Update the docstring with the new assumption.
- Stay deterministic with a fixed `seed`.

## Questions

Open a discussion or comment on the issue. Maintainers review PRs and merge.
