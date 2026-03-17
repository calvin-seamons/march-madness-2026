# March Madness 2026 Bracket Engine

A data-driven bracket prediction system that generates 20 strategically diverse NCAA tournament brackets using a multi-source ensemble model calibrated against Vegas odds.

**3.6% average deviation from Vegas implied probabilities** across all 32 first-round games.

---

## How It Works

### The Ensemble Model

The algorithm blends **three independent power rating systems** — the same approach FiveThirtyEight used (they blended six). Each system captures different signal:

| System                                | Weight | What It Measures                                 |
| ------------------------------------- | ------ | ------------------------------------------------ |
| **Bart Torvik** (T-Rank)              | 40%    | Tempo-adjusted efficiency with recency weighting |
| **Sports Reference** Adjusted Ratings | 30%    | SRS-based adjusted offensive/defensive ratings   |
| **ESPN BPI**                          | 30%    | Proprietary model with 10,000 simulations        |

### On Top of the Ensemble

The base power ratings feed into a **Log5 head-to-head probability model**, then get adjusted for:

- **Injury impact** — star player losses quantified (e.g., Texas Tech losing Toppin dropped their defense from 24th to 119th)
- **Momentum** — last 10 games performance vs season average
- **Luck regression** — teams that overperformed in close games regress (KenPom luck has only 0.06 year-to-year correlation)
- **Coaching tournament experience** — 10+ NCAA appearances provides measurable edge
- **Turnover vulnerability** — +1% turnover rate = 42% higher upset odds (Harvard Sports Analysis)
- **3PT defense** — poor perimeter D is the #1 upset indicator
- **Offensive rebounding** — second chances keep underdogs alive
- **Free throw shooting** — champions average 71.9% vs 70.1% field average

### Calibrated Against Vegas

The model auto-calibrates its adjustment weights to minimize RMSE against Vegas implied odds for all 32 Round of 64 games — ensuring our probabilities are grounded in the sharpest market in sports.

### 50,000 Simulations → 20 Brackets

The calibrated model runs a full **Monte Carlo simulation** of the tournament 50,000 times, then generates 20 brackets with strategic diversity:

- **Brackets 1-3:** Maximum likelihood (chalk) with the top 3 most likely champions
- **Brackets 4-10:** Probability-weighted sampling targeting specific champions
- **Brackets 11-16:** Slight upset lean for coverage
- **Brackets 17-20:** Heavier upset injection for Cinderella scenarios

---

## Data Sources

| Source            | Data                                          | File                          |
| ----------------- | --------------------------------------------- | ----------------------------- |
| Bart Torvik       | AdjOE, AdjDE, AdjT, barthag for 365 teams     | `data/barttorvik_2026.csv`    |
| Sports Reference  | Four Factors, shooting splits, opponent stats | `data/sports_reference_*.csv` |
| ESPN BPI API      | BPI, Off/Def BPI, title %, SOR for 365 teams  | `data/espn_bpi_all_teams.csv` |
| Vegas Sportsbooks | Round of 64 implied probabilities             | Hardcoded in `team_data.py`   |

---

## Quick Start

```bash
# Install dependency
pip install openpyxl

# Run everything — calibrate, simulate, generate, export
python main.py
```

Output: `output/march_madness_2026_brackets.xlsx`

The spreadsheet contains:

- **Advancement Probabilities** — every team's % to reach each round
- **Champion Distribution** — which champions appear across the 20 brackets
- **Championship Totals Matrix** — projected combined score for every possible title matchup
- **20 Individual Bracket Sheets** — every game, every round, with upset markers
- **All Brackets Comparison** — side-by-side view of all 20 brackets

---

## 2026 Model Output

### Championship Probabilities

```
(1) Duke                  20.8%  ██████████
(1) Michigan              15.6%  ███████
(1) Arizona               14.6%  ███████
(1) Florida                9.9%  ████
(2) Houston                6.9%  ███
(3) Illinois               5.6%  ██
(2) Purdue                 5.3%  ██
(2) Iowa State             5.1%  ██
(2) UConn                  1.4%
(3) Michigan State         1.8%
```

### First Round Upset Watch

```
(9) Iowa over (8) Clemson               54%
(9) Utah State over (8) Villanova       54%
(10) Santa Clara over (7) Kentucky      51%
(9) Saint Louis over (8) Georgia        47%
(11) Texas/NC State over (6) BYU        44%
(10) Missouri over (7) Miami FL         42%
(12) Akron over (5) Texas Tech          21%
```

---

## Project Structure

```
march-madness-2026/
├── main.py              # Entry point — runs the full pipeline
├── algorithm.py         # Ensemble model, Log5, adjustments, calibration
├── simulator.py         # Monte Carlo engine + bracket generation
├── team_data.py         # 68 tournament teams, bracket structure, Vegas odds
├── load_real_data.py    # Loads Torvik, SR, ESPN data into the model
├── export_brackets.py   # Excel export with formatting
├── data/                # Raw data files (CSV, JSON)
│   ├── barttorvik_2026.csv
│   ├── espn_bpi_all_teams.csv
│   ├── sports_reference_*.csv
│   └── ...
└── output/
    └── march_madness_2026_brackets.xlsx
```

---

## Research Backing

The model design is informed by:

- **FiveThirtyEight's methodology** — ensemble of 6 rating systems + human polls + injury adjustments
- **KenPom** — Pythagorean win probability with exponent 10.25
- **Bill James's Log5** — head-to-head probability from independent win rates
- **Harvard Sports Analysis Collective** — turnover rate (+42% upset odds per 1%), 3PT defense (+28%), offensive rebounding (+13%)
- **Historical seed data (1985-2025)** — 160 games per seed matchup as Bayesian priors
- **Kaggle March ML Mania** — logistic regression consistently wins; ensemble > single model

---

_Built with Claude Code. Data current as of Selection Sunday, March 15, 2026._
