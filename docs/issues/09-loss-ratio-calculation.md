# Issue #9 — Incorrect loss-ratio calculation (Medium)

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/pricing.py` (`compute_loss_ratio`)
- **Relevant public test:** `tests/test_pricing.py::test_loss_ratio_uses_earned_premium`

## Problem description
The denominator sums premiums without multiplying by members,
so earned premium is wildly understated and the loss ratio inflated
(the starter report shows thousands of percent).

## Expected behaviour
Loss ratio = total payouts / sum(premium x members) per zone.

## Acceptance criteria
- [ ] Denominator uses earned premium (premium x members).
- [ ] Zero earned premium → 0.0 (no division by zero).
- [ ] `python -m mazhai.main` loss ratio becomes a sane value.

## Reproduction steps
1. `pytest tests/test_pricing.py::test_loss_ratio_uses_earned_premium -v`
2. `python -m mazhai.main` (note absurd loss ratio)
