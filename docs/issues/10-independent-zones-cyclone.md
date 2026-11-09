# Issue #10 — Independent-zone assumption in cyclone simulation (Hard)

- **Difficulty:** Hard
- **Affected file:** `src/mazhai/simulation.py` (`run_monte_carlo`)
- **Relevant public test:** smoke test via `python -m mazhai.main` (Monte-Carlo section)

## Problem description
Zones are simulated with independent draws, so a single cyclone never
hits all zones in the same week. Real storms are spatially correlated
— tail (p95) portfolio loss is understated.

## Expected behaviour
Add a shared storm factor / correlation so cyclone weeks hit multiple
zones together; document the new assumption in the module docstring.

## Acceptance criteria
- [ ] Cyclone weeks produce correlated zone triggers.
- [ ] `run_monte_carlo` signature stays compatible & deterministic.
- [ ] p95 portfolio payout rises vs the independent baseline.
- [ ] Docstring lists the new assumption.

## Reproduction steps
1. `python -m mazhai.main` (note p95 under independence)
