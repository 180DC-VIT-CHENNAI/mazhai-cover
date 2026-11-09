"""Payout tests — Issues #5 (duplicate), #6 (weekly cap), #7 (subsidy)."""

from mazhai import payouts


def _event(zone="Z1", start="2026-01-01T10:00:00", end="2026-01-01T11:00:00"):
    return {"zone_id": zone, "start_time": start, "end_time": end, "peak_mm": 25.0}


def test_basic_payout_amount():
    # PASSING baseline.
    assert payouts.calculate_payout(_event()) == 500.0
    assert payouts.total_payouts([_event(), _event(start="2026-01-02T10:00:00")]) == 1000.0


def test_duplicate_events_collapse_to_one():
    # Issue #5: same zone + spell repeated must pay once.
    e = _event()
    events = [e, dict(e), dict(e)]
    assert len(payouts.deduplicate_events(events)) == 1


def test_weekly_cap_enforced():
    # Issue #6: cap 1000 with 500/payout allows at most 2 payouts.
    events = [_event(start=f"2026-01-0{i}T10:00:00") for i in range(1, 6)]
    capped = payouts.apply_weekly_cap(events, weekly_cap=1000.0)
    assert len(capped) == 2
    assert payouts.total_payouts(capped) <= 1000.0


def test_subsidy_only_for_eligible_riders():
    # Issue #7: eligible gets subsidy, non-eligible gets nothing.
    assert payouts.calculate_subsidy(eligible=True) == 50.0
    assert payouts.calculate_subsidy(eligible=False) == 0.0
