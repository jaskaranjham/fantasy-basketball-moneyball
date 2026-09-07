# Fantasy Basketball Moneyball Draft Board

A Python based fantasy basketball draft board that evaluates NBA players using my ESPN league's custom scoring settings.

This project marks my return to coding and analytics. The goal is to take a Moneyball inspired approach to fantasy basketball by measuring both total fantasy production and how broadly a player contributes.

## V1 Goals

V1 uses last season's NBA statistics to answer:

1. Who produced the most fantasy points per game under my league's scoring rules?
2. Who produced value across multiple areas instead of relying mainly on one strength?

V1 does not include rookies, predictions, ADP, injury forecasting, or upcoming season projections.

## League Scoring

- Points: +1
- Field goals made: +2
- Field goals attempted: -1
- Free throws made: +1
- Free throws attempted: -1
- Three-pointers made: +1
- Rebounds: +1
- Assists: +2
- Steals: +4
- Blocks: +4
- Turnovers: -2

## Contribution Areas

- Scoring
- Rebounding
- Playmaking
- Defence

Each area is converted into a percentile so players can be compared across categories with different statistical scales.

## Current Rankings

- Fantasy PPG Rank: pure fantasy production
- Maximum Value Rank: fantasy production adjusted for across-the-board contribution

## Current Model Limitation

The initial 70/30 production versatility formula ranked Jalen Johnson above Shai Gilgeous-Alexander. This revealed that percentile-based production compressed meaningful fantasy point differences and allowed versatility to have too much influence.

The next model iteration will rebalance the formula so versatility acts as a tiebreaker between similarly productive players.

## Data Source

NBA player statistics are retrieved from ESPN using pandas.

## Future Versions

- Rookie evaluation using college and Summer League data
- Upcoming-season projections
- Draft assistance
- Roster construction
- Free agent replacement recommendations