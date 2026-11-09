# Issue #8 — Zone premium exceeds 2.5x cap (Medium)

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/pricing.py` (`enforce_premium_cap`)
- **Relevant public tests:** `tests/test_pricing.py::test_premium_cap_2_5x_enforced`, `test_zone_premiums_via_pipeline_respects_cap`

## Problem description
`enforce_premium_cap` is a no-op, so high-risk zones quote premiums
far above 2.5x the cheapest zone, violating the product requirement.

## Expected behaviour
`max(premiums) <= 2.5 * min(premiums)` after enforcement.

## Acceptance criteria
- [ ] Capped premiums satisfy the 2.5x rule.
- [ ] Cheapest zone unchanged.
- [ ] Empty/single-zone inputs don't crash.

## Reproduction steps
1. `pytest tests/test_pricing.py -k cap -v`
