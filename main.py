#!/usr/bin/env python3
"""
March Madness 2026 Bracket Generator
=====================================

Generates 20 strategically diverse brackets using:
1. KenPom AdjEM-based power ratings
2. Log5 head-to-head probability model
3. Multi-factor adjustments (injuries, momentum, coaching, luck regression,
   turnover vulnerability, 3PT defense, rebounding, free throws)
4. Calibration against Vegas implied odds
5. Historical seed-based Bayesian priors
6. 50,000 Monte Carlo tournament simulations
7. Strategic bracket diversity for optimal coverage

Usage:
    python main.py
"""

import random
from algorithm import calibrate, predict_game
from simulator import (
    TournamentSimulator,
    BracketGenerator,
    print_advancement_table,
    print_bracket,
    count_upsets_in_bracket,
)
from export_brackets import export_to_excel, export_to_csv
from team_data import TEAMS, BRACKET_MATCHUPS
from load_real_data import update_teams_with_real_data


def main():
    # Set seed for reproducibility (change for different bracket sets)
    random.seed(2026)

    print("=" * 70)
    print("  MARCH MADNESS 2026 — BRACKET PREDICTION ENGINE")
    print("  50,000 Monte Carlo Simulations | 20 Strategic Brackets")
    print("=" * 70)
    print()

    # =========================================================================
    # PHASE 0: Load real data from Torvik + Sports Reference
    # =========================================================================
    print("PHASE 0: Loading real data (Bart Torvik + Sports Reference)...")
    print("-" * 70)
    updated, missing = update_teams_with_real_data(TEAMS)
    print(f"  Updated {updated} teams with real Torvik/SR data")
    if missing:
        print(f"  Missing from data sources: {missing}")
    print()

    # Also update the algorithm's pace/efficiency dicts with real data
    from algorithm import TEAM_PACE, TEAM_EFFICIENCY
    for team_name, team_info in TEAMS.items():
        if "_real_adjt" in team_info:
            TEAM_PACE[team_name] = team_info["_real_adjt"]
        if "_real_adjoe" in team_info:
            TEAM_EFFICIENCY[team_name] = (team_info["_real_adjoe"], team_info["_real_adjde"])

    # =========================================================================
    # PHASE 1: Calibrate model against Vegas
    # =========================================================================
    print("PHASE 1: Calibrating model against Vegas implied odds...")
    print("-" * 70)
    optimal_scale = calibrate(verbose=True)
    print()

    # =========================================================================
    # PHASE 2: Run Monte Carlo simulation
    # =========================================================================
    print("PHASE 2: Running Monte Carlo simulation...")
    print("-" * 70)

    sim = TournamentSimulator(calibration_scale=optimal_scale)
    n_sims = 50000
    advancement, champions, all_brackets = sim.run_monte_carlo(
        n_simulations=n_sims, verbose=True
    )

    # Print advancement probabilities
    print("\nTEAM ADVANCEMENT PROBABILITIES:")
    print_advancement_table(advancement, n_sims, top_n=40)

    # =========================================================================
    # PHASE 3: Generate 20 brackets
    # =========================================================================
    print("\nPHASE 3: Generating 20 strategic brackets...")
    print("-" * 70)

    generator = BracketGenerator(sim, optimal_scale)
    brackets = generator.generate_20_brackets(advancement, champions, n_sims)

    # Print summary of all brackets
    print("\n" + "=" * 70)
    print("BRACKET SUMMARY")
    print("=" * 70)
    print(f"{'#':<4} {'Strategy':<45} {'Champion':<20} {'Upsets':<8}")
    print("-" * 77)
    for b in brackets:
        num = b.get("_number", "?")
        strategy = b.get("_strategy", "")[:44]
        champion = b["Champion"]
        seed = TEAMS[champion]["seed"]
        upsets = count_upsets_in_bracket(b)
        print(f"{num:<4} {strategy:<45} ({seed}) {champion:<16} {upsets}")

    # Print first 3 brackets in detail
    print("\n\nDETAILED VIEW — TOP 3 BRACKETS:")
    for b in brackets[:3]:
        print_bracket(b)

    # =========================================================================
    # PHASE 4: Export to spreadsheet
    # =========================================================================
    print("\n\nPHASE 4: Exporting to spreadsheet...")
    print("-" * 70)

    try:
        export_to_excel(brackets, advancement, champions, n_sims)
    except Exception as e:
        print(f"Excel export failed ({e}), falling back to CSV...")
        export_to_csv(brackets, advancement, champions, n_sims)

    # =========================================================================
    # PHASE 5: Key insights
    # =========================================================================
    print("\n" + "=" * 70)
    print("KEY INSIGHTS FROM THE MODEL")
    print("=" * 70)

    # Top championship contenders
    print("\nChampionship Probabilities:")
    for team, count in champions.most_common(10):
        seed = TEAMS[team]["seed"]
        pct = count / n_sims * 100
        bar = "█" * int(pct / 2)
        print(f"  ({seed}) {team:<20} {pct:>5.1f}% {bar}")

    # Most likely Final Four
    print("\nMost Likely Final Four Participants:")
    ff_probs = []
    for team in TEAMS:
        ff_count = advancement[team].get("FF", 0)
        if ff_count > 0:
            ff_probs.append((team, ff_count / n_sims))
    ff_probs.sort(key=lambda x: x[1], reverse=True)
    for team, prob in ff_probs[:12]:
        seed = TEAMS[team]["seed"]
        region = TEAMS[team]["region"]
        bar = "█" * int(prob * 50)
        print(f"  ({seed}) {team:<20} [{region:<7}] {prob:>5.1%} {bar}")

    # First round upset picks ranked by probability
    print("\nFirst Round Upset Watch (model probabilities):")
    upset_candidates = []
    for region in BRACKET_MATCHUPS:
        for team_a, team_b in BRACKET_MATCHUPS[region]:
            seed_a = TEAMS[team_a]["seed"]
            seed_b = TEAMS[team_b]["seed"]
            if seed_a < seed_b:  # A is favored by seed
                prob_upset = 1 - predict_game(team_a, team_b, "R64", optimal_scale)
                if prob_upset > 0.10:
                    upset_candidates.append((team_b, team_a, seed_b, seed_a, prob_upset))
            else:
                prob_upset = predict_game(team_a, team_b, "R64", optimal_scale)
                if prob_upset > 0.10 and seed_a > seed_b:
                    upset_candidates.append((team_a, team_b, seed_a, seed_b, prob_upset))

    upset_candidates.sort(key=lambda x: x[4], reverse=True)
    for underdog, favorite, seed_u, seed_f, prob in upset_candidates[:15]:
        bar = "█" * int(prob * 50)
        print(f"  ({seed_u}) {underdog:<18} over ({seed_f}) {favorite:<18} {prob:>5.1%} {bar}")

    # Where model disagrees most with Vegas
    print("\nBiggest Model vs Vegas Disagreements (potential edges):")
    from team_data import VEGAS_ODDS_R64
    disagreements = []
    for (team_a, team_b), (vegas_a, vegas_b) in VEGAS_ODDS_R64.items():
        if team_a in TEAMS and team_b in TEAMS:
            model_a = predict_game(team_a, team_b, "R64", optimal_scale)
            diff = model_a - vegas_a
            if abs(diff) > 0.02:
                disagreements.append((team_a, team_b, model_a, vegas_a, diff))
    disagreements.sort(key=lambda x: abs(x[4]), reverse=True)
    for team_a, team_b, model, vegas, diff in disagreements[:10]:
        seed_a = TEAMS[team_a]["seed"]
        seed_b = TEAMS[team_b]["seed"]
        direction = "↑" if diff > 0 else "↓"
        team_favored = team_a if diff > 0 else team_b
        print(f"  ({seed_a}) {team_a} vs ({seed_b}) {team_b}: "
              f"Model {model:.1%} vs Vegas {vegas:.1%} "
              f"({direction} {abs(diff):.1%} on {team_favored})")

    print("\n" + "=" * 70)
    print("  Done! Check the output/ folder for your spreadsheet.")
    print("=" * 70)


if __name__ == "__main__":
    main()
