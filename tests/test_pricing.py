"""Pricing tests — Issues #8 (2.5x cap) and #9 (loss ratio)."""

from mazhai import pricing
from mazhai.data_loader import Zone


def _zone(zone_id="Z1", members=1000, risk=0.5):
    return Zone(
        zone_id=zone_id,
        zone_name="Test",
        city="Chennai",
        risk_score=risk,
        base_premium_monthly=150.0,
        weekly_payout_cap=50000.0,
        members=members,
    )


def test_base_premium_formula():
    # PASSING baseline: expected/ members * 1.2 + 30.
    z = _zone(members=1000)
    assert pricing.calculate_base_premium(z, 10000.0) == round(12000 / 1000 + 30, 2)


def test_premium_cap_2_5x_enforced():
    # Issue #8: max premium <= 2.5x the cheapest.
    premiums = {"Z1": 100.0, "Z2": 400.0}  # 400 > 250
    capped = pricing.enforce_premium_cap(premiums)
    assert max(capped.values()) <= 2.5 * min(capped.values())


def test_loss_ratio_uses_earned_premium():
    # Issue #9: earned = premium x members.
    zones = [_zone("Z1", members=1000), _zone("Z2", members=2000)]
    premiums = {"Z1": 100.0, "Z2": 150.0}
    earned = 100 * 1000 + 150 * 2000  # 400,000
    assert pricing.compute_loss_ratio(200_000.0, zones, premiums) == 200_000.0 / earned


def test_zone_premiums_via_pipeline_respects_cap():
    # Issue #8 via calculate_zone_premiums: skewed payouts must not breach cap.
    zones = [_zone("Z1", members=1000), _zone("Z2", members=1000)]
    payouts_by_zone = {"Z1": 0.0, "Z2": 2_000_000.0}
    premiums = pricing.calculate_zone_premiums(zones, payouts_by_zone)
    assert max(premiums.values()) <= 2.5 * min(premiums.values())
