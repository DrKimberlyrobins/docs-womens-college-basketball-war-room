# DOC'S WOMEN'S COLLEGE BASKETBALL WAR ROOM

**STATUS: UNDER CONSTRUCTION — NOT VALIDATED FOR FORECASTING**

This repository is independent of the men's basketball and NBA War Rooms.

## Implemented
- Experimental independent full-game possession-based engine with 10,000 seeded stochastic simulations.
- Explicit rejection of missing statistics.
- Responsive dashboard shell that does not invent game predictions.
- Unit tests and a GitHub Actions test workflow.

## Experimental mathematics
Expected possessions = harmonic mean of team tempos.
Projected points per possession = team adjusted offense × opponent adjusted defense / 10,000.
Simulations sample correlated offensive efficiency variation and possession variation.
The model is **not calibrated** and must not be used for betting decisions.
No sportsbook data enters forecast calculations.

## Not yet implemented or verified
- Authorized schedules, team ratings, player data and sportsbook integrations.
- Independently calibrated first-half and quarter models.
- Immutable pregame forecast archive, postgame ingestion, grading and accuracy dashboard.
- Historical out-of-sample validation, browser E2E tests, live GitHub Pages verification.

Production forecasts remain withheld until legitimate source data and validation exist.
