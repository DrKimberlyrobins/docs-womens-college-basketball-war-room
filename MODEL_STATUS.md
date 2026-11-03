# Forecast model acceptance gates

## Full-game
Implemented: seeded stochastic simulations and projected score distribution.
Not complete: empirical training, injury effects, venue, roster turnover, pace calibration, game-level validation.

## First-half and quarters
Implemented: separate period-specific simulation accepting four independently estimated historical priors.
Not complete: the period priors have **no connected data source**, and are not yet fitted or backtested. The system will reject missing period priors rather than divide a full-game projection by two.

## Sportsbook
Implemented: independent model/market numerical comparisons and two-way no-vig implied probability.
Not complete: licensed odds feeds and timestamped pregame quote capture.

## Results and grading
Implemented: historical CSV integrity checks, snapshot persistence, final-only grade function, summary error metrics.
Not complete: live verified provider connection, scheduled automatic ingestion, durable Git commits for generated archives, comprehensive historical out-of-sample evaluation.

No production-ready prediction claims should be made until all relevant acceptance gates pass.
