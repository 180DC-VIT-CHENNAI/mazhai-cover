# Mazhai Cover — Open-Source Starter

Mazhai (மழை) means "rain" in Tamil. Mazhai Cover is a **parametric micro-insurance**
starter for gig delivery riders in Chennai, workshopped as an open-source
collaboration project. It is deliberately incomplete: you can install and run
it immediately, but several financial-logic bugs and missing features are
seeded as GitHub issues for contributors to fix together.

> This repository is a **starting point for collaboration**, not an evaluation
> platform. Tests and CI exist so contributors can verify their work, not to
> rank teams.

## Quick Start

```bash
pip install -r requirements.txt
pip install -e .
python -m mazhai.main
pytest
python -m flask --app "mazhai.api:create_app" run --host 127.0.0.1 --port 5000
# then open http://127.0.0.1:5000/ for the dashboard
```

`python -m mazhai.main` prints an insurance pricing report (premiums, payouts,
loss ratio, and Monte-Carlo tail risk). Some tests pass; others fail because
of the seeded bugs listed in [Known Issues](#known-issues-12-contributor-tasks).
Fixing issues makes the corresponding tests pass.

## Product Requirements (from the Mazhai Cover case)

These are **product rules of the insurance**, not judging criteria:

| Rule | Value |
|---|---|
| Trigger | Rainfall ≥ 20 mm in **2 consecutive hours** in the rider's zone |
| Payout per trigger | ₹500 flat (parametric, no loss adjustment) |
| Zone premium cap | Max zone premium ≤ **2.5×** the cheapest zone premium |
| Weekly payout cap | Per-zone weekly payouts capped (see `zones.csv` → `weekly_payout_cap`) |
| Subsidy | ₹50/month rider subsidy for eligible riders only (see `riders.csv`) |
| Loss ratio | `total payouts / total earned premium` (earned = premium × members) |

## Repository Layout

```
data/                         # synthetic CSVs (seeded, deterministic)
  rainfall.csv                # timestamp, zone_id, rainfall_mm, rainfall_unit
  zones.csv                   # zone pricing + payout caps
  riders.csv                  # rider enrolment + subsidy eligibility
src/mazhai/
  data_loader.py              # CSV loading, unit conversion, missing-data handling
  triggers.py                 # consecutive-hour parametric trigger
  payouts.py                  # payout calc, dedup, weekly cap, subsidy
  pricing.py                  # zone premiums, 2.5x cap, loss ratio, optimiser
  simulation.py               # Monte-Carlo risk simulation
  api.py                      # Flask API + static frontend host
  main.py                     # CLI: builds the pricing report
frontend/
  index.html, app.js, style.css  # React 18 dashboard (CDN, no bundler)
tests/                        # public tests (contributor verification)
.github/                      # issue templates + CI (public tests only)
docs/issues/                  # markdown for GitHub issues
```

## Architecture

```
rainfall.csv → data_loader → triggers → payouts → pricing → main report
                                          ↑           ↑
                                   riders/zones  simulation
```

- **data_loader**: parses CSVs, converts units, handles missing values.
- **triggers**: detects 2-consecutive-hour events per zone.
- **payouts**: one ₹500 payout per event, deduped, weekly-capped, with subsidies.
- **pricing**: monthly zone premiums from expected payouts; enforces 2.5× cap;
  computes loss ratio; optimises premium with enrolment elasticity.
- **simulation**: Monte-Carlo over synthetic weekly rainfall to estimate tail risk.
- **api**: Flask endpoints (`/api/report`, `/api/simulate`, `/webhooks/rainfall`) serving the dashboard.
- **frontend**: React dashboard loading `/api/report` and `/api/simulate` (CDN, no build).

## Simulation Assumptions & Limitations

`src/mazhai/simulation.py` ships a **basic working simulation** so the repo
runs from Day 0. Documented assumptions (see module docstring):

- Zones are treated as independent (cyclone correlation is Issue #10).
- Rainfall distribution is stationary/static (climate trend is Issue #11).
- Synthetic data is illustrative, not calibrated weather.

Contributors improving correlation or extreme-rainfall modelling should
update the docstring and keep `run_monte_carlo` backward compatible.

## Known Issues — 12 Contributor Tasks

| # | Issue | Difficulty | Module |
|---|---|---|---|
| 1 | Rainfall unit conversion error (cm read as mm) | Easy | `data_loader.py` |
| 2 | Missing rainfall handling (treated as 0) | Easy | `data_loader.py` |
| 3 | Consecutive-hour counter resets at midnight | Medium | `triggers.py` |
| 4 | Incorrect single-hour trigger | Medium | `triggers.py` |
| 5 | Duplicate payouts for same event | Medium | `payouts.py` |
| 6 | Weekly payout cap ignored | Medium | `payouts.py` |
| 7 | Incorrect subsidy calculation | Easy | `payouts.py` |
| 8 | Zone premium exceeds 2.5× cap | Medium | `pricing.py` |
| 9 | Incorrect loss-ratio calculation | Medium | `pricing.py` |
| 10 | Independent-zone assumption in cyclone simulation | Hard | `simulation.py` |
| 11 | Static rainfall distribution (ignores trend) | Hard | `simulation.py` |
| 12 | Enrolment elasticity missing from pricing | Hard | `pricing.py` |

Each issue in `docs/issues/` contains: problem description, affected file,
expected behaviour, acceptance criteria, reproduction steps, and relevant
public test where applicable. Open them as GitHub issues to pick them up.

## Hackathon Day Timeline (suggested)

| Time | Activity |
|---|---|
| 0–30 min | Clone and understand architecture |
| 30 min–2 hours | Fix simpler bugs |
| 2–5 hours | Work on triggers, payouts and pricing |
| 5–7 hours | Improve simulation and implement missing features |
| 7–8 hours | Complete PRs and demonstrate the solution |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). In short: pick an issue, branch,
fix, run `pytest`, open a PR. CI runs the public tests.

## License

MIT — see [LICENSE](./LICENSE).
