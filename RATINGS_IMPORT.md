# Complete all-matchup statistical join

`team_stats.py` ingests a **permitted** season ratings CSV with columns:
`team,adj_off,adj_def,tempo`.

It joins every game in `data/dashboard.json` using normalized names and a reviewed alias file, runs 10,000 stochastic draws for each matchup where **both** teams are present, and reports unmatched teams rather than inventing statistics.

Run:
```bash
python team_stats.py --ratings data/authorized_team_ratings.csv --source "licensed provider" --as-of "2026-11-03T09:00:00-06:00" --aliases data/team_aliases.json
```

The CSV is not bundled because no verified license or comprehensive 2025–26 ratings export has been supplied. GitHub Actions fails visibly if the export is missing. Projections remain experimental pending held-out calibration and roster adjustments. Do not interpret the mere presence of a projected number as an independently validated betting edge.
