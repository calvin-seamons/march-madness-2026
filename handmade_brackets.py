#!/usr/bin/env python3
"""
Generate 4 hand-crafted brackets optimized for pool winning.

Each bracket has a different champion from the top 4 contenders.
Upset counts calibrated to historical averages (~8-9 R64, ~12-15 total).

Historical R64 upset distribution:
  8/9 games: ~2 of 4 go to 9-seed (historically 9s lead 83-77)
  5/12 games: ~1.4 of 4 are upsets (35.6% rate)
  6/11 games: ~1.5 of 4 are upsets (38.7% rate)
  7/10 games: ~1.5 of 4 are upsets (38.7% rate)
  3/14 games: ~0.6 of 4 (14.4% rate)
  4/13 games: ~0.8 of 4 (20.6% rate)
  2/15 games: ~0.3 of 4 (6.9% rate)
  1/16 games: ~0.05 of 4 (1.2% rate)
"""

from team_data import TEAMS, BRACKET_MATCHUPS
from algorithm import predict_game_total


def make_bracket(r64, r32, s16, e8, ff, champion, name, tiebreaker=None):
    """Construct a bracket dict from picks."""
    regions = ["East", "South", "West", "Midwest"]
    bracket = {"_strategy": name, "_number": name}

    for i, region in enumerate(regions):
        bracket[region] = {
            "R64": r64[region],
            "R32": r32[region],
            "S16": s16[region],
            "E8": e8[region],
        }

    bracket["FF"] = ff
    bracket["Champion"] = champion

    # Calculate tiebreaker (projected total)
    finalist_a = ff[0]
    finalist_b = ff[1]
    _, _, total = predict_game_total(finalist_a, finalist_b, is_championship=True)
    bracket["_tiebreaker"] = tiebreaker or round(total)

    return bracket


# ============================================================================
# BRACKET A: DUKE CHAMPION (most likely winner at 21.2%)
# Strategy: Chalk-heavy but with historically expected upsets
# Target: ~8 R64 upsets, ~13 total upsets
# ============================================================================

bracket_a = make_bracket(
    name="Bracket A — Duke National Champion",
    r64={
        "East": ["Duke", "TCU",  # 9 over 8 Ohio State (39% model)
                "St. John's", "Kansas",
                "Louisville", "Michigan State", "UCLA", "UConn"],
        "South": ["Florida", "Iowa",  # 9 Iowa over 8 Clemson (54% model)
                  "Vanderbilt", "Nebraska",
                  "North Carolina", "Illinois",
                  "Texas A&M",  # 10 over 7 Saint Mary's (42% model)
                  "Houston"],
        "West": ["Arizona", "Utah State",  # 9 Utah St over 8 Nova (55% model)
                "Wisconsin", "Arkansas",
                "BYU", "Gonzaga", "Miami FL", "Purdue"],
        "Midwest": ["Michigan", "Saint Louis",  # 9 over 8 Georgia (46% model)
                   "Texas Tech", "Alabama",
                   "Tennessee", "Virginia",
                   "Santa Clara",  # 10 over 7 Kentucky (45% model)
                   "Iowa State"],
    },
    r32={
        "East": ["Duke", "St. John's", "Michigan State", "UConn"],
        "South": ["Florida", "Vanderbilt", "Illinois", "Houston"],
        "West": ["Arizona", "Arkansas", "Gonzaga", "Purdue"],
        "Midwest": ["Michigan", "Alabama", "Virginia", "Iowa State"],
    },
    s16={
        "East": ["Duke", "UConn"],
        "South": ["Florida", "Houston"],
        "West": ["Arizona", "Purdue"],
        "Midwest": ["Michigan", "Iowa State"],
    },
    e8={
        "East": "Duke",
        "South": "Houston",
        "West": "Arizona",
        "Midwest": "Michigan",
    },
    ff=["Duke", "Michigan"],  # South/East → Duke, Midwest/West → Michigan
    champion="Duke",
)


# ============================================================================
# BRACKET B: MICHIGAN CHAMPION
# Strategy: Slightly more upsets, Michigan dominates Midwest
# Target: ~9 R64 upsets, ~14 total upsets
# ============================================================================

bracket_b = make_bracket(
    name="Bracket B — Michigan National Champion",
    r64={
        "East": ["Duke", "TCU",  # 9 TCU over 8 Ohio State (39% model)
                "St. John's", "Kansas",
                "Louisville", "Michigan State", "UCLA", "UConn"],
        "South": ["Florida", "Iowa",  # 9 Iowa over 8 Clemson
                  "Vanderbilt", "Nebraska",
                  "VCU",  # 11 VCU over 6 North Carolina (41% model)
                  "Illinois", "Texas A&M",  # 10 over 7 St Mary's (42% model)
                  "Houston"],
        "West": ["Arizona", "Utah State",  # 9 over 8
                "Wisconsin", "Arkansas",
                "Texas/NC State",  # 11 over 6 BYU (38% model)
                "Gonzaga", "Missouri",  # 10 over 7 Miami (38% model)
                "Purdue"],
        "Midwest": ["Michigan", "Saint Louis",  # 9 over 8 Georgia (46% model)
                   "Texas Tech", "Alabama",
                   "Tennessee", "Virginia", "Kentucky", "Iowa State"],
    },
    r32={
        "East": ["Duke", "St. John's", "Michigan State", "UConn"],
        "South": ["Florida", "Vanderbilt", "Illinois", "Houston"],
        "West": ["Arizona", "Arkansas", "Gonzaga", "Purdue"],
        "Midwest": ["Michigan", "Alabama", "Virginia", "Iowa State"],
    },
    s16={
        "East": ["Duke", "UConn"],
        "South": ["Florida", "Houston"],
        "West": ["Arizona", "Purdue"],
        "Midwest": ["Michigan", "Iowa State"],
    },
    e8={
        "East": "Duke",
        "South": "Florida",
        "West": "Arizona",
        "Midwest": "Michigan",
    },
    ff=["Duke", "Michigan"],  # South/East → Duke, Midwest/West → Michigan
    champion="Michigan",
)


# ============================================================================
# BRACKET C: ARIZONA CHAMPION
# Strategy: Arizona dominates West, more upsets elsewhere
# Target: ~10 R64 upsets, ~15 total upsets
# ============================================================================

bracket_c = make_bracket(
    name="Bracket C — Arizona National Champion",
    r64={
        "East": ["Duke", "TCU",  # 9 over 8
                "St. John's", "Kansas",
                "South Florida",  # 11 over 6 Louisville (24% model)
                "Michigan State", "UCF",  # 10 over 7 UCLA (27% model)
                "UConn"],
        "South": ["Florida", "Iowa",  # 9 over 8
                  "McNeese",  # 12 over 5 Vanderbilt (19% model)
                  "Nebraska",
                  "North Carolina", "Illinois", "Saint Mary's", "Houston"],
        "West": ["Arizona", "Utah State",  # 9 over 8
                "Wisconsin", "Arkansas",
                "BYU", "Gonzaga", "Miami FL", "Purdue"],
        "Midwest": ["Michigan", "Georgia",
                   "Akron",  # 12 over 5 Texas Tech (25% model — Toppin out)
                   "Alabama",
                   "Tennessee", "Virginia",
                   "Santa Clara",  # 10 over 7 Kentucky (45% model)
                   "Iowa State"],
    },
    r32={
        "East": ["Duke", "St. John's", "Michigan State", "UConn"],
        "South": ["Florida", "Nebraska", "Illinois", "Houston"],
        "West": ["Arizona", "Arkansas", "Gonzaga", "Purdue"],
        "Midwest": ["Michigan", "Alabama", "Virginia", "Iowa State"],
    },
    s16={
        "East": ["Duke", "UConn"],
        "South": ["Florida", "Houston"],
        "West": ["Arizona", "Gonzaga"],
        "Midwest": ["Michigan", "Iowa State"],
    },
    e8={
        "East": "Duke",
        "South": "Houston",
        "West": "Arizona",
        "Midwest": "Michigan",
    },
    ff=["Duke", "Arizona"],  # South/East → Duke, Midwest/West → Arizona
    champion="Arizona",
)


# ============================================================================
# BRACKET D: FLORIDA CHAMPION (defending champ, hot streak)
# Strategy: Florida runs the South, more chaos elsewhere
# Target: ~10 R64 upsets, ~16 total upsets
# ============================================================================

bracket_d = make_bracket(
    name="Bracket D — Florida National Champion (Defending Champ)",
    r64={
        "East": ["Duke", "Ohio State",
                "St. John's", "Kansas",
                "South Florida",  # 11 over 6 Louisville
                "Michigan State",
                "UCF",  # 10 over 7 UCLA
                "UConn"],
        "South": ["Florida", "Iowa",  # 9 over 8
                  "Vanderbilt", "Nebraska",
                  "VCU",  # 11 over 6 North Carolina (Wilson out, 0-2 without him)
                  "Illinois",
                  "Texas A&M",  # 10 over 7 Saint Mary's
                  "Houston"],
        "West": ["Arizona", "Utah State",  # 9 over 8
                "Wisconsin", "Arkansas",
                "Texas/NC State",  # 11 over 6 BYU (Saunders out)
                "Gonzaga",
                "Missouri",  # 10 over 7 Miami FL
                "Purdue"],
        "Midwest": ["Michigan", "Saint Louis",  # 9 over 8 Georgia
                   "Texas Tech", "Alabama",
                   "Miami OH/SMU",  # 11 over 6 Tennessee
                   "Virginia",
                   "Santa Clara",  # 10 over 7 Kentucky
                   "Iowa State"],
    },
    r32={
        "East": ["Duke", "St. John's", "Michigan State", "UConn"],
        "South": ["Florida", "Vanderbilt", "Illinois", "Houston"],
        "West": ["Arizona", "Arkansas", "Gonzaga", "Purdue"],
        "Midwest": ["Michigan", "Alabama", "Virginia", "Iowa State"],
    },
    s16={
        "East": ["Duke", "UConn"],
        "South": ["Florida", "Illinois"],
        "West": ["Arizona", "Purdue"],
        "Midwest": ["Michigan", "Iowa State"],
    },
    e8={
        "East": "Duke",
        "South": "Florida",  # Florida beats Illinois — defending champ grit
        "West": "Arizona",
        "Midwest": "Michigan",
    },
    ff=["Florida", "Arizona"],  # South/East → Florida (upsets Duke), Midwest/West → Arizona
    champion="Florida",
)


ALL_BRACKETS = [bracket_a, bracket_b, bracket_c, bracket_d]


if __name__ == "__main__":
    from simulator import count_upsets_in_bracket, print_bracket

    for b in ALL_BRACKETS:
        upsets = count_upsets_in_bracket(b)
        champ = b["Champion"]
        seed = TEAMS[champ]["seed"]
        tb = b["_tiebreaker"]
        print(f"\n{'='*70}")
        print(f"{b['_strategy']}")
        print(f"Upsets: {upsets}  |  Tiebreaker: {tb}")
        print(f"{'='*70}")
        print_bracket(b)
