# Fantasy Basketball Moneyball Draft Board

A Python-based fantasy basketball draft board that evaluates NBA players using my ESPN league's custom scoring settings.

This project marks my return to coding and analytics. The goal is to take a Moneyball-inspired approach to fantasy basketball by measuring both total fantasy production and how broadly a player contributes.

## V1 Goals

V1 uses last season's NBA statistics to answer:

1. Who produced the most fantasy points per game under my league's scoring rules?
2. Who produced value across multiple areas instead of relying mainly on one strength?

V1 does not include rookies, predictions, ADP, injury forecasting or upcoming season projections.

## Qualified Player Pool

To reduce misleading results from small samples and limited playing time, V1 includes players who averaged at least:

- 20 games played
- 15 minutes per game

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

## Contribution Percentiles

Player production is divided into four areas:

- Scoring
- Rebounding
- Playmaking
- Defence

Each contribution is converted into a percentile relative to the qualified player pool.

### Across the Board Score

The four contribution percentiles are combined using a harmonic mean. This rewards players who contribute strongly across every area while allowing a major weakness to lower the overall score.

The Across the Board Score measures the balance of a player's production, not their total fantasy points.

### Production Score

Fantasy PPG is normalized to a 0–100 scale using the minimum and maximum Fantasy PPG among qualified players.

This preserves the actual production difference between players instead of treating all highly ranked players as nearly equal.

### Maximum Value Score

The final score uses:

- 70% Production Score
- 30% Across the Board Score

Maximum Value Rank orders players by their combination of total fantasy production and balanced contribution.

## Model Testing

The initial model converted Fantasy PPG into a percentile. This compressed meaningful differences between elite players and allowed Jalen Johnson's balance to move him above Shai Gilgeous-Alexander.

The revised model normalizes the actual Fantasy PPG range. This preserves Shai's production advantage while still rewarding Jalen's broader contribution profile.

The weighting remains an experimental modelling decision and may be refined through further basketball and statistical validation.

## Output

The program creates `fantasy_draft_board_v1.xlsx`, containing:

- Fantasy PPG Rank
- Maximum Value Rank
- Fantasy PPG
- Production Score
- Across the Board Score
- Maximum Value Score
- Scoring percentile
- Rebounding percentile
- Playmaking percentile
- Defensive percentile
- The underlying per-game statistics

## Data Source

NBA player statistics are retrieved from ESPN using pandas. V1 is explicitly pinned to the 2025–26 NBA regular season.

## Running the Project

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python main.py
```

The generated draft board will appear in the project folder as `fantasy_draft_board_v1.xlsx`.

## Current Limitations

- V1 uses historical per game statistics.
- Rookies without NBA statistics are not included.
- The model does not account for injuries, offseason roster changes or projected roles.
- The 70/30 weighting is an experimental modelling decision.

## Future Versions

- Rookie evaluation using college and Summer League data
- Upcoming-season projections
- Draft assistance
- Roster construction
- Free-agent replacement recommendations