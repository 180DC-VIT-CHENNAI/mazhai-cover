# Issue #12 — Enrolment elasticity missing from pricing (Hard)

- **Difficulty:** Hard
- **Affected file:** `src/mazhai/pricing.py` (`find_optimal_premium`)
- **Relevant public test:** none yet — add one (see below)

## Problem description
`find_optimal_premium` returns break-even regardless of price.
Raising premiums reduces rider enrolment
(`members(p) ~ baseline * (p/base)**elasticity`), so a high "optimum"
can shrink the book to near zero.

## Expected behaviour
Model enrolment elasticity and choose the premium maximising
earned premium net of expected payouts.

## Acceptance criteria
- [ ] Enrolment curve implemented (elasticity param respected).
- [ ] Optimum is interior (not simply the highest premium tried).
- [ ] New public test shows higher premium → fewer members.
- [ ] Docstring documents the demand model + defaults.

## Reproduction steps
1. Inspect `find_optimal_premium` — `elasticity` is accepted but unused.
