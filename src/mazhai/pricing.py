"""Zone premiums, 2.5x cap, loss ratio, and premium optimisation.

Product requirements:
- Max zone premium <= 2.5x the cheapest zone premium.
- Loss ratio = total payouts / total earned premium,
  where earned premium = premium x members (per zone, summed).
- Optimisation must account for enrolment elasticity: raising the
  premium reduces uptake, so the "optimal" premium balances
  per-member payout cover against members who actually enrol.
"""

from __future__ import annotations

from mazhai.data_loader import Zone

PREMIUM_CAP_MULTIPLIER = 2.5


def calculate_base_premium(zone: Zone, expected_monthly_payouts: float) -> float:
    """Baseline premium covering expected payouts + 20% loading, flat ₹30 cost floor."""
    per_member = expected_monthly_payouts / max(zone.members, 1)
    return round(per_member * 1.2 + 30.0, 2)


def enforce_premium_cap(premiums: dict[str, float]) -> dict[str, float]:
    """Cap every zone premium at 2.5x the minimum premium."""
    # TODO(Issue #8): the 2.5x restriction is not enforced.
    # Currently out-of-cap premiums pass through unchanged.
    return dict(premiums)  # BUG: cap not applied


def calculate_zone_premiums(
    zones: list[Zone], payouts_by_zone: dict[str, float]
) -> dict[str, float]:
    premiums = {
        z.zone_id: calculate_base_premium(z, payouts_by_zone.get(z.zone_id, 0.0))
        for z in zones
    }
    return enforce_premium_cap(premiums)


def compute_loss_ratio(
    total_payouts: float, zones: list[Zone], premiums: dict[str, float]
) -> float:
    """total payouts / total earned premium (premium x members, summed)."""
    earned = sum(premiums.get(z.zone_id, 0.0) * z.members for z in zones)
    if earned <= 0:
        return 0.0
    # TODO(Issue #9): wrong denominator — members are ignored, understating
    # earned premium and inflating the loss ratio.
    wrong_denominator = sum(premiums.get(z.zone_id, 0.0) for z in zones)  # BUG
    if wrong_denominator <= 0:
        return 0.0
    _ = earned  # computed (correct) but unused due to the bug
    return total_payouts / wrong_denominator


def find_optimal_premium(
    base_premium: float,
    expected_monthly_payouts: float,
    members: int,
    elasticity: float = -0.8,
    baseline_members: int | None = None,
) -> float:
    """Naive optimum ignoring enrolment elasticity (see Issue #12).

    Currently returns the break-even premium regardless of how many
    riders drop out as price rises. A correct implementation should
    model members(p) = baseline * (p / base) ** elasticity and pick
    the premium maximising earned cover net of payouts.
    """
    # TODO(Issue #12): enrolment elasticity is ignored.
    per_member = expected_monthly_payouts / max(members, 1)
    return round(per_member * 1.2 + 30.0, 2)  # BUG: returns base_premium-equivalent


def premium_with_subsidy(premium: float, subsidy: float) -> float:
    """Effective premium a subsidised rider actually pays."""
    return max(premium - subsidy, 0.0)
