"""Mazhai Cover pricing report CLI.

Run: python -m mazhai.main
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from mazhai import data_loader, payouts, pricing, triggers
from mazhai.simulation import run_monte_carlo


def _data_dir() -> Path:
    root = Path(__file__).resolve().parents[2]
    for candidate in (root / "data", Path("data")):
        if candidate.exists():
            return candidate
    return root / "data"


def build_report(data_dir: Path | None = None) -> str:
    data = data_dir or _data_dir()
    rainfall = data_loader.load_rainfall(data / "rainfall.csv")
    zones = data_loader.load_zones(data / "zones.csv")
    riders = data_loader.load_riders(data / "riders.csv")

    events = triggers.detect_events(rainfall)
    events = payouts.deduplicate_events(events)

    # Per-zone payout totals with weekly cap applied (Issue #6).
    zone_events: dict[str, list[dict]] = defaultdict(list)
    for e in events:
        zone_events[e["zone_id"]].append(e)

    payouts_by_zone: dict[str, float] = {}
    for zone in zones:
        capped = payouts.apply_weekly_cap(
            zone_events.get(zone.zone_id, []), zone.weekly_payout_cap
        )
        payouts_by_zone[zone.zone_id] = payouts.total_payouts(capped)

    premiums = pricing.calculate_zone_premiums(zones, payouts_by_zone)
    total_payout = sum(payouts_by_zone.values())
    loss_ratio = pricing.compute_loss_ratio(total_payout, zones, premiums)
    sim = run_monte_carlo(zones, n_simulations=200, seed=42)

    cheapest = min(premiums.values()) if premiums else 0.0
    lines = []
    lines.append("=" * 60)
    lines.append("Mazhai Cover - Pricing Report (starter, known bugs present)")
    lines.append("=" * 60)
    lines.append(
        f"Zones: {len(zones)}  Riders: {len(riders)}  Events: {len(events)}"
    )
    lines.append("")
    lines.append(
        f"{'Zone':<28} {'Risk':>6} {'Members':>8} {'Payout':>10} {'Premium':>10}"
    )
    for zone in zones:
        p = premiums.get(zone.zone_id, 0.0)
        lines.append(
            f"{zone.zone_name:<28} {zone.risk_score:>6.2f} {zone.members:>8} "
            f"{payouts_by_zone.get(zone.zone_id, 0.0):>10.0f} {p:>10.2f}"
        )
    lines.append("")
    lines.append(f"Total payouts: Rs.{total_payout:,.0f}")
    lines.append(f"Loss ratio:    {loss_ratio:.2%}  (see Issue #9)")
    if cheapest:
        lines.append(
            f"Cheapest premium: Rs.{cheapest:.2f}  "
            f"Max allowed (2.5x): Rs.{cheapest * 2.5:.2f}"
        )
        over = {
            zid: p
            for zid, p in premiums.items()
            if p > cheapest * 2.5
        }
        if over:
            lines.append(f"2.5x cap breached (Issue #8): {over}")
    lines.append("")
    lines.append("Monte-Carlo (200 sims, independent zones - Issue #10):")
    lines.append(
        f"  Portfolio mean payout: Rs.{sim['portfolio']['mean_payout']:,.0f}"
    )
    lines.append(
        f"  Portfolio p95 payout:  Rs.{sim['portfolio']['p95_payout']:,.0f}"
    )
    lines.append("")
    lines.append("See README.md > Known Issues for the 12 contributor tasks.")
    return "\n".join(lines)


def main() -> None:
    print(build_report())


if __name__ == "__main__":
    main()
