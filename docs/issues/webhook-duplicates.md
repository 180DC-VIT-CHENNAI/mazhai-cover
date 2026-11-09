# Some webhook events are processed more than once

- **Difficulty:** Medium
- **Affected file:** `src/mazhai/api.py` (webhooks)
- **Relevant public test:** `tests/test_api.py::test_webhook_accepts_fixture`

## Problem description
The same rainfall event delivered twice adds payouts twice.

## Expected behaviour
Duplicate deliveries of the same event ID are recognised and counted once.

## Acceptance criteria
- [ ] Retries with same event ID do not double-count.
- [ ] New event IDs still process normally.

## Reproduction steps
1. POST the same local fixture twice; observe weekly totals.
