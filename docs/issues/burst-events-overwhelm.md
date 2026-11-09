# A burst of rainfall events overwhelms the API

- **Difficulty:** Hard
- **Affected file:** `src/mazhai/api.py` (webhooks)
- **Relevant public test:** `tests/test_api.py::test_webhook_accepts_fixture`

## Problem description
A burst of webhook events makes the API slow/unresponsive.

## Expected behaviour
Bursts queue, coalesce, or shed load with backpressure; service stays up.

## Acceptance criteria
- [ ] Burst of local events keeps health endpoint responsive.
- [ ] Events are eventually processed or clearly shed.

## Reproduction steps
1. Burst local webhook POSTs and poll `/api/health`.
