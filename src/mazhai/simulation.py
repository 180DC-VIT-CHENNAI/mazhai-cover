"""Monte-Carlo simulation of zone risk and portfolio loss.

Basic working simulation so the repo runs from Day 0.

Assumptions (documented for contributors):
1. Weekly rainfall per zone ~ Normal(mean = risk_score * 60 mm, sd = 25 mm),
   truncated at 0. Each simulated week above the 2-hour trigger
   threshold yields one payout.
2. Zones are modelled INDEPENDENTLY (no storm correlation).
3. The rainfall distribution is STATIONARY (no climate trend over time).
4. Synthetic data is illustrative, not calibrated weather.

Known limitations are contributor tasks:
- Issue #10: add cyclone correlation so a single storm hits zones together.
- Issue #11: add an extreme-rainfall trend so future years are wetter.

Improving either should keep ``run_monte_carlo`` signature-compatible and
update this docstring.
"""

from __future__ import annotations

import numpy as np

from mazhai.data_loader import Zone

PAYOUT_PER_TRIGGER = 500.0
TRIGGER_WEEKLY_MM = 80.0  # weekly rainfall proxy for a trigger week


def run_monte_carlo(
    zones: list[Zone],
    n_simulations: int = 200,
    n_weeks: int = 52,
    seed: int = 42,
) -> dict:
    """Simulate portfolio payouts over ``n_weeks``.

    Returns per-zone mean/p95 payouts and portfolio-level summary.
    """
    rng = np.random.default_rng(seed)
    # NOTE: independent per-zone draws — no shared storm factor (Issue #10).
    # NOTE: static mean — no trend term (Issue #11).
    zone_results: dict[str, dict] = {}
    portfolio_totals = np.zeros(n_simulations)

    for zone in zones:
        mean_mm = zone.risk_score * 60.0
        weekly = rng.normal(mean_mm, 25.0, size=(n_simulations, n_weeks))
        weekly = np.clip(weekly, 0, None)
        triggers = (weekly > TRIGGER_WEEKLY_MM).sum(axis=1)
        payouts = triggers * PAYOUT_PER_TRIGGER
        portfolio_totals += payouts
        zone_results[zone.zone_id] = {
            "mean_payout": float(payouts.mean()),
            "p95_payout": float(np.percentile(payouts, 95)),
            "mean_triggers": float(triggers.mean()),
        }

    return {
        "n_simulations": n_simulations,
        "n_weeks": n_weeks,
        "zones": zone_results,
        "portfolio": {
            "mean_payout": float(portfolio_totals.mean()),
            "p95_payout": float(np.percentile(portfolio_totals, 95)),
            "max_payout": float(portfolio_totals.max()),
        },
        "assumptions": [
            "independent zones",
            "stationary rainfall distribution",
            "weekly rainfall ~ Normal(risk*60, 25), truncated at 0",
        ],
    }
