"""Payouts: fixed amount per trigger, deduped, weekly-capped, subsidised.

Rules:
- One payout per rainfall event (no double-paying the same spell).
- Weekly total per zone must not exceed the zone's weekly cap.
- Subsidy applies only to subsidy-eligible riders.
"""

from __future__ import annotations

DEFAULT_PAYOUT = 500.0
DEFAULT_SUBSIDY = 50.0


def calculate_payout(event: dict, payout_amount: float = DEFAULT_PAYOUT) -> float:
    return float(payout_amount)


def deduplicate_events(events: list[dict]) -> list[dict]:
    """Remove duplicate events for the same zone + spell.

    Identity is (zone_id, start_time, end_time).
    """
    # TODO(Issue #5): duplicates for the same event must collapse to one.
    # Currently events are returned untouched, so overlapping windows
    # produce multiple payouts for one spell.
    return list(events)  # BUG: no dedup


def apply_weekly_cap(
    events: list[dict], weekly_cap: float, payout_amount: float = DEFAULT_PAYOUT
) -> list[dict]:
    """Keep at most ``weekly_cap // payout_amount`` payouts.

    Assumes all events fall in the same week for the starter pipeline;
    fixes should group by ISO week when touching this area.
    """
    # TODO(Issue #6): the weekly cap is not enforced — all events pass.
    return list(events)  # BUG: cap ignored


def calculate_subsidy(eligible: bool, subsidy_amount: float = DEFAULT_SUBSIDY) -> float:
    # TODO(Issue #7): subsidy must go ONLY to eligible riders.
    # Currently the flag is inverted (non-eligible riders get paid).
    return 0.0 if eligible else float(subsidy_amount)  # BUG: inverted


def total_payouts(events: list[dict], payout_amount: float = DEFAULT_PAYOUT) -> float:
    return sum(calculate_payout(e, payout_amount) for e in events)
