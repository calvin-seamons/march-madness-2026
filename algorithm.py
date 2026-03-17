"""
March Madness 2026 Prediction Algorithm
Multi-factor model calibrated against Vegas odds.

Methodology:
1. Convert KenPom AdjEM to base win probabilities (Log5)
2. Apply situational adjustments (injuries, momentum, coaching, luck regression)
3. Calibrate against Vegas implied odds
4. Blend with historical seed-based Bayesian priors
"""

import math
from team_data import TEAMS, VEGAS_ODDS_R64, HISTORICAL_SEED_WIN_RATES


# =============================================================================
# STEP 1: Convert KenPom AdjEM to a "strength" rating
# =============================================================================

def kenpom_em_to_win_pct(em, team_name=None):
    """
    Convert power rating to an expected win percentage against an average D-I team.

    ENSEMBLE APPROACH (like FiveThirtyEight):
    Blends multiple independent rating systems:
      - Torvik barthag (40% weight) — best single predictor, tempo-adjusted
      - SR Adjusted Net Rating (30% weight) — independent SRS-based system
      - ESPN BPI (30% weight) — ESPN's proprietary model with 10K simulations

    FiveThirtyEight found that blending 6 systems outperformed any single one.
    Three independent systems should capture most of the benefit.
    """
    if team_name and team_name in TEAMS:
        t = TEAMS[team_name]
        estimates = []
        weights = []

        # Source 1: Torvik barthag (pre-computed Pythagorean win probability)
        if "_real_barthag" in t:
            estimates.append(t["_real_barthag"])
            weights.append(0.40)

        # Source 2: Sports Reference Adjusted Net Rating (independent system)
        if "_sr_adj_nrtg" in t:
            sr_nrtg = t["_sr_adj_nrtg"]
            sr_win_pct = 1.0 / (1.0 + 10 ** (-sr_nrtg / 17.0))
            estimates.append(sr_win_pct)
            weights.append(0.30)

        # Source 3: ESPN BPI (ESPN's proprietary power index)
        if "_espn_bpi" in t:
            bpi = t["_espn_bpi"]
            # BPI range: ~-25 (worst) to ~+26 (best)
            # Scale of 16.9 optimized against Vegas R64 odds
            bpi_win_pct = 1.0 / (1.0 + 10 ** (-bpi / 16.9))
            estimates.append(bpi_win_pct)
            weights.append(0.30)

        # Fallback: SRS if we have fewer than 2 sources
        if "_real_srs" in t and len(estimates) < 2:
            srs = t["_real_srs"]
            srs_win_pct = 1.0 / (1.0 + 10 ** (-srs / 12.0))
            estimates.append(srs_win_pct)
            weights.append(0.20)

        if estimates:
            total_weight = sum(weights)
            blended = sum(e * w for e, w in zip(estimates, weights)) / total_weight
            return max(0.001, min(0.999, blended))

    # Fallback: logistic function on efficiency margin
    scale = 15.0
    win_pct = 1.0 / (1.0 + 10 ** (-em / scale))
    return max(0.001, min(0.999, win_pct))


# =============================================================================
# STEP 2: Log5 Head-to-Head Probability
# =============================================================================

def log5(p_a, p_b):
    """
    Bill James's Log5 method for head-to-head probability.

    Given:
      p_a = Team A's win probability vs average opponent
      p_b = Team B's win probability vs average opponent

    Returns: probability that A beats B
    """
    numerator = p_a * (1 - p_b)
    denominator = p_a * (1 - p_b) + p_b * (1 - p_a)

    if denominator == 0:
        return 0.5

    return numerator / denominator


# =============================================================================
# STEP 3: Situational Adjustment Factors
# =============================================================================

def compute_adjustment(team_a, team_b):
    """
    Compute a log-odds adjustment for Team A vs Team B based on
    situational factors. Returns adjustment in log-odds space.

    Positive = favors team A, Negative = favors team B.
    """
    a = TEAMS[team_a]
    b = TEAMS[team_b]
    adjustment = 0.0

    # --- Injury Impact ---
    # Injury factor 0-1 scale. Convert to points equivalent.
    # A significant injury (star player out) is ~3-8 point swing.
    # We use up to 5 points equivalent in log-odds
    injury_diff = b["injury_factor"] - a["injury_factor"]  # Positive if B more injured
    adjustment += injury_diff * 4.0  # Points equivalent

    # --- Momentum / Hot-Cold Streak ---
    # Scale: -1 (ice cold) to +1 (on fire)
    # Research shows limited but non-zero predictive value
    # Weight: up to ~1.5 points equivalent
    momentum_diff = a["momentum"] - b["momentum"]
    adjustment += momentum_diff * 0.8

    # --- KenPom Luck Regression ---
    # High luck teams (>0.04) have won more close games than expected.
    # Regress toward mean — penalize high-luck teams.
    # r=0.06 year-to-year, so almost all luck regresses.
    luck_penalty_a = max(0, a["luck"] - 0.02) * 15  # Penalize excess luck
    luck_penalty_b = max(0, b["luck"] - 0.02) * 15
    adjustment += luck_penalty_b - luck_penalty_a  # Favors A if B has more excess luck

    # --- Coaching Tournament Experience ---
    # 10+ appearances provides measurable advantage.
    # Effect: ~0.5-1.5 points for experienced coaches
    coach_a = min(a["coach_tourney_exp"], 20)
    coach_b = min(b["coach_tourney_exp"], 20)
    coach_bonus = (coach_a - coach_b) * 0.06  # Diminishing returns
    adjustment += coach_bonus

    # --- Turnover Vulnerability (for favorites) ---
    # High TO rate increases upset odds by 42% per 1%.
    # Only applies meaningfully when there's a significant quality gap.
    em_diff = a["kenpom_em"] - b["kenpom_em"]
    if em_diff > 5:  # A is significantly favored
        # Penalize A for high turnover rate
        to_vulnerability = (a["to_rate"] - 0.16) * 8  # 0.16 is "average"
        adjustment -= max(0, to_vulnerability)
    elif em_diff < -5:  # B is significantly favored
        to_vulnerability = (b["to_rate"] - 0.16) * 8
        adjustment += max(0, to_vulnerability)

    # --- 3PT Defense Vulnerability ---
    # Poor 3PT defense (+1% allowed) = 28% higher upset odds
    if em_diff > 5:  # A favored — check A's 3PT defense vulnerability
        three_pt_vuln = (a["opp_fg_pct_3pt"] - 0.32) * 6
        adjustment -= max(0, three_pt_vuln)
    elif em_diff < -5:  # B favored
        three_pt_vuln = (b["opp_fg_pct_3pt"] - 0.32) * 6
        adjustment += max(0, three_pt_vuln)

    # --- Offensive Rebounding Advantage ---
    # Especially important for underdogs — second chances keep them alive
    oreb_diff = a["oreb_pct"] - b["oreb_pct"]
    adjustment += oreb_diff * 3.0

    # --- Free Throw Shooting ---
    # Matters in close games, especially late-tournament
    ft_diff = a["ft_pct"] - b["ft_pct"]
    adjustment += ft_diff * 2.0

    return adjustment


# =============================================================================
# STEP 4: Combined Win Probability
# =============================================================================

def predict_game(team_a, team_b, round_name="R64", calibration_scale=1.0):
    """
    Predict the probability that team_a beats team_b.

    Process:
    1. Convert KenPom AdjEM to base win probabilities
    2. Use Log5 for head-to-head probability
    3. Apply situational adjustments
    4. Blend with historical seed rates (Bayesian prior)
    5. Return calibrated probability

    Args:
        team_a: Name of team A
        team_b: Name of team B
        round_name: Tournament round (for weighting historical priors)
        calibration_scale: Scaling factor for adjustments (tuned against Vegas)

    Returns:
        Probability that team_a wins (0 to 1)
    """
    a = TEAMS[team_a]
    b = TEAMS[team_b]

    # Step 1: Base win probabilities from KenPom/Torvik
    p_a = kenpom_em_to_win_pct(a["kenpom_em"], team_name=team_a)
    p_b = kenpom_em_to_win_pct(b["kenpom_em"], team_name=team_b)

    # Step 2: Log5 head-to-head
    base_prob = log5(p_a, p_b)

    # Step 3: Situational adjustments (in log-odds space)
    adjustment = compute_adjustment(team_a, team_b) * calibration_scale

    # Convert base probability to log-odds, apply adjustment, convert back
    # log-odds = log(p / (1-p))
    base_prob = max(0.001, min(0.999, base_prob))
    log_odds = math.log(base_prob / (1 - base_prob))

    # Scale adjustment: 1 "point" adjustment ≈ 0.08 in log-odds
    # (based on empirical relationship: 1 point spread ≈ 3% win probability near 50%)
    adjusted_log_odds = log_odds + adjustment * 0.08

    # Convert back to probability
    model_prob = 1 / (1 + math.exp(-adjusted_log_odds))

    # Step 4: Blend with historical seed rates (Bayesian prior)
    # Weight: 85% model, 15% historical in R64
    # Reduce historical weight in later rounds (less relevant data)
    seed_a = a["seed"]
    seed_b = b["seed"]

    historical_weight = 0.15 if round_name == "R64" else 0.08
    seed_key = (min(seed_a, seed_b), max(seed_a, seed_b))

    if seed_key in HISTORICAL_SEED_WIN_RATES:
        hist_prob = HISTORICAL_SEED_WIN_RATES[seed_key]
        if seed_a > seed_b:  # A is the higher seed number (lower ranked)
            hist_prob = 1 - hist_prob
        final_prob = (1 - historical_weight) * model_prob + historical_weight * hist_prob
    else:
        final_prob = model_prob

    return max(0.001, min(0.999, final_prob))


# =============================================================================
# STEP 5: Calibration Against Vegas
# =============================================================================

def calibrate(verbose=True):
    """
    Find the optimal calibration_scale that minimizes RMSE
    between our model's R64 predictions and Vegas implied odds.

    Returns the optimal calibration scale.
    """
    best_scale = 1.0
    best_rmse = float('inf')

    for scale_x100 in range(50, 200, 1):  # 0.50 to 2.00
        scale = scale_x100 / 100.0
        total_sq_error = 0
        count = 0

        for (team_a, team_b), (vegas_a, vegas_b) in VEGAS_ODDS_R64.items():
            if team_a not in TEAMS or team_b not in TEAMS:
                continue
            model_prob = predict_game(team_a, team_b, "R64", calibration_scale=scale)
            error = (model_prob - vegas_a) ** 2
            total_sq_error += error
            count += 1

        rmse = (total_sq_error / count) ** 0.5 if count > 0 else float('inf')

        if rmse < best_rmse:
            best_rmse = rmse
            best_scale = scale

    if verbose:
        print(f"Calibration complete: scale={best_scale:.2f}, RMSE={best_rmse:.4f}")
        print(f"Average deviation from Vegas: {best_rmse*100:.1f} percentage points")
        print()

        # Show comparison for each game
        print("=" * 85)
        print(f"{'Matchup':<40} {'Model':>8} {'Vegas':>8} {'Diff':>8}")
        print("=" * 85)
        for (team_a, team_b), (vegas_a, vegas_b) in sorted(
            VEGAS_ODDS_R64.items(),
            key=lambda x: abs(
                predict_game(x[0][0], x[0][1], "R64", best_scale) - x[1][0]
            ),
            reverse=True
        ):
            if team_a not in TEAMS or team_b not in TEAMS:
                continue
            model_p = predict_game(team_a, team_b, "R64", best_scale)
            diff = model_p - vegas_a
            marker = " ***" if abs(diff) > 0.05 else ""
            a_seed = TEAMS[team_a]["seed"]
            b_seed = TEAMS[team_b]["seed"]
            matchup = f"({a_seed}) {team_a} vs ({b_seed}) {team_b}"
            print(f"{matchup:<40} {model_p:>7.1%} {vegas_a:>7.1%} {diff:>+7.1%}{marker}")
        print("=" * 85)
        print("*** = deviation > 5 percentage points (potential edge)")

    return best_scale


# =============================================================================
# STEP 6: Projected Point Total for a Matchup
# =============================================================================

# Pace (possessions per 40 min) for key teams. Source: Sports-Reference 2025-26
# Teams not listed default to national average (~68.0)
TEAM_PACE = {
    "Duke": 67.1, "Michigan": 71.3, "Arizona": 71.3, "Florida": 72.5,
    "Houston": 64.9, "Iowa State": 68.2, "UConn": 66.0, "Purdue": 65.3,
    "Illinois": 66.2, "Michigan State": 68.5, "Gonzaga": 69.0,
    "Virginia": 62.5, "Nebraska": 66.8, "Alabama": 73.5,
    "Kansas": 67.5, "Arkansas": 70.0, "St. John's": 65.5,
    "Vanderbilt": 69.5, "Wisconsin": 65.0, "Texas Tech": 66.5,
    "Tennessee": 64.0, "North Carolina": 71.0, "Louisville": 68.0,
    "BYU": 69.5, "Kentucky": 70.0, "Saint Mary's": 63.5,
    "Miami FL": 67.5, "UCLA": 68.5,
}

# Approximate AdjO and AdjD (points per 100 possessions) for key teams
# Source: KenPom/Sports-Reference 2025-26 estimates
TEAM_EFFICIENCY = {
    # team: (AdjO, AdjD)  — lower AdjD = better defense
    "Duke":           (122.6, 82.1),
    "Michigan":       (126.4, 87.1),
    "Arizona":        (120.3, 83.0),
    "Florida":        (119.8, 86.0),
    "Houston":        (118.4, 83.2),
    "Iowa State":     (120.0, 85.2),
    "UConn":          (116.5, 86.4),
    "Purdue":         (124.7, 90.0),
    "Illinois":       (125.5, 95.0),
    "Michigan State": (115.0, 90.5),
    "Gonzaga":        (118.0, 88.0),
    "Virginia":       (112.0, 88.5),
    "Nebraska":       (113.5, 92.0),
    "Alabama":        (120.5, 100.5),
    "Kansas":         (108.0, 88.5),
    "Arkansas":       (117.0, 95.0),
    "St. John's":     (114.0, 93.0),
    "Vanderbilt":     (116.0, 95.5),
    "Wisconsin":      (113.0, 94.5),
    "Texas Tech":     (110.0, 94.0),
    "Tennessee":      (107.0, 89.0),
    "North Carolina": (115.0, 97.5),
    "Louisville":     (114.0, 96.0),
    "BYU":            (115.5, 98.5),
    "Kentucky":       (112.0, 97.0),
    "Saint Mary's":   (109.0, 92.5),
    "Miami FL":       (113.0, 97.5),
    "UCLA":           (112.5, 96.5),
}

# National average efficiency (2025-26 season)
NATIONAL_AVG_EFFICIENCY = 105.0

# Championship game depression factor:
# - Under hits 55% of the time historically
# - Dome effect suppresses shooting by ~3-5%
# - Average recent title game total: 139.0 (vs ~145 historical)
# - Extra rest day favors defensive preparation
CHAMPIONSHIP_TOTAL_DEPRESSION = 0.96  # ~4% lower than raw projection


def predict_game_total(team_a, team_b, is_championship=False):
    """
    Predict the combined point total for a matchup.

    Uses KenPom-style formula:
      Expected Possessions = avg of both teams' pace
      Team A Score = (AdjO_A / 100) * (AdjD_B / NatAvg) * Possessions
      Team B Score = (AdjO_B / 100) * (AdjD_A / NatAvg) * Possessions

    Returns: (team_a_score, team_b_score, combined_total)
    """
    nat_avg = NATIONAL_AVG_EFFICIENCY
    default_pace = 68.0

    pace_a = TEAM_PACE.get(team_a, default_pace)
    pace_b = TEAM_PACE.get(team_b, default_pace)
    expected_poss = (pace_a + pace_b) / 2

    # Get efficiencies, default to deriving from KenPom EM
    if team_a in TEAM_EFFICIENCY:
        adj_o_a, adj_d_a = TEAM_EFFICIENCY[team_a]
    else:
        em_a = TEAMS[team_a]["kenpom_em"]
        adj_o_a = nat_avg + em_a / 2
        adj_d_a = nat_avg - em_a / 2

    if team_b in TEAM_EFFICIENCY:
        adj_o_b, adj_d_b = TEAM_EFFICIENCY[team_b]
    else:
        em_b = TEAMS[team_b]["kenpom_em"]
        adj_o_b = nat_avg + em_b / 2
        adj_d_b = nat_avg - em_b / 2

    # Score projections
    score_a = (adj_o_a / 100) * (adj_d_b / nat_avg) * expected_poss
    score_b = (adj_o_b / 100) * (adj_d_a / nat_avg) * expected_poss

    total = score_a + score_b

    # Apply championship game depression (dome effect, defensive intensity, rest day)
    if is_championship:
        total *= CHAMPIONSHIP_TOTAL_DEPRESSION
        score_a *= CHAMPIONSHIP_TOTAL_DEPRESSION
        score_b *= CHAMPIONSHIP_TOTAL_DEPRESSION

    return round(score_a, 1), round(score_b, 1), round(total, 1)


# =============================================================================
# Quick test
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MARCH MADNESS 2026 — ALGORITHM CALIBRATION")
    print("=" * 60)
    print()

    optimal_scale = calibrate(verbose=True)

    print()
    print("=" * 60)
    print("SAMPLE PREDICTIONS (using calibrated model)")
    print("=" * 60)
    print()

    # Test some interesting matchups from later rounds
    test_matchups = [
        ("Duke", "Michigan"),
        ("Duke", "Arizona"),
        ("Michigan", "Arizona"),
        ("Duke", "Florida"),
        ("Houston", "Florida"),
        ("UConn", "St. John's"),
        ("Texas Tech", "Akron"),
        ("North Carolina", "VCU"),
        ("Kentucky", "Santa Clara"),
    ]

    for a, b in test_matchups:
        if a in TEAMS and b in TEAMS:
            prob = predict_game(a, b, "R64", optimal_scale)
            print(f"  {a} vs {b}: {a} wins {prob:.1%}")
