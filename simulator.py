"""
Monte Carlo Tournament Simulator & Bracket Generator

Simulates 50,000 full tournaments using calibrated win probabilities,
then generates 20 strategically diverse brackets.
"""

import random
import math
from collections import defaultdict, Counter
from algorithm import predict_game, calibrate
from team_data import TEAMS, BRACKET_MATCHUPS, ESPN_SCORING


# =============================================================================
# TOURNAMENT SIMULATION
# =============================================================================

class TournamentSimulator:
    """
    Simulates the full NCAA tournament using calibrated win probabilities.
    """

    def __init__(self, calibration_scale=1.0):
        self.scale = calibration_scale
        self.regions = ["East", "West", "South", "Midwest"]

        # Final Four pairings (2026 bracket)
        # South vs East, Midwest vs West
        self.ff_matchups = [("South", "East"), ("Midwest", "West")]

    def simulate_game(self, team_a, team_b, round_name="R64"):
        """Simulate a single game. Returns the winner."""
        prob_a = predict_game(team_a, team_b, round_name, self.scale)
        if random.random() < prob_a:
            return team_a
        return team_b

    def simulate_region(self, region_name):
        """
        Simulate all games within a region through the Elite 8.
        Returns list of winners for each round and the region champion.
        """
        matchups = BRACKET_MATCHUPS[region_name]
        results = {"R64": [], "R32": [], "S16": [], "E8": None}

        # Round of 64 (8 games per region)
        r64_winners = []
        for team_a, team_b in matchups:
            winner = self.simulate_game(team_a, team_b, "R64")
            r64_winners.append(winner)
        results["R64"] = list(r64_winners)

        # Round of 32 (4 games): game 0 vs game 1, game 2 vs game 3, etc.
        r32_winners = []
        for i in range(0, 8, 2):
            winner = self.simulate_game(r64_winners[i], r64_winners[i + 1], "R32")
            r32_winners.append(winner)
        results["R32"] = list(r32_winners)

        # Sweet 16 (2 games): game 0 vs game 1, game 2 vs game 3
        s16_winners = []
        for i in range(0, 4, 2):
            winner = self.simulate_game(r32_winners[i], r32_winners[i + 1], "S16")
            s16_winners.append(winner)
        results["S16"] = list(s16_winners)

        # Elite 8 (1 game)
        e8_winner = self.simulate_game(s16_winners[0], s16_winners[1], "E8")
        results["E8"] = e8_winner

        return results

    def simulate_tournament(self):
        """
        Simulate a full 63-game tournament.
        Returns a complete bracket with all results.
        """
        bracket = {}

        # Simulate each region
        region_champions = {}
        for region in self.regions:
            results = self.simulate_region(region)
            bracket[region] = results
            region_champions[region] = results["E8"]

        # Final Four
        ff_results = []
        for region_a, region_b in self.ff_matchups:
            winner = self.simulate_game(
                region_champions[region_a],
                region_champions[region_b],
                "FF"
            )
            ff_results.append(winner)
        bracket["FF"] = ff_results

        # Championship
        champion = self.simulate_game(ff_results[0], ff_results[1], "CG")
        bracket["Champion"] = champion

        return bracket

    def run_monte_carlo(self, n_simulations=50000, verbose=True):
        """
        Run Monte Carlo simulation of the full tournament.

        Returns:
            advancement: dict of team -> {round: count} showing how many
                         times each team advanced to each round
            champions: Counter of championship winners
            all_brackets: list of all simulated brackets
        """
        advancement = defaultdict(lambda: defaultdict(int))
        champions = Counter()
        all_brackets = []

        if verbose:
            print(f"Running {n_simulations:,} tournament simulations...")

        for i in range(n_simulations):
            if verbose and (i + 1) % 10000 == 0:
                print(f"  Completed {i + 1:,} simulations...")

            bracket = self.simulate_tournament()
            all_brackets.append(bracket)

            # Track advancement
            for region in self.regions:
                results = bracket[region]

                # R64 winners
                for team in results["R64"]:
                    advancement[team]["R32"] += 1

                # R32 winners
                for team in results["R32"]:
                    advancement[team]["S16"] += 1

                # S16 winners
                for team in results["S16"]:
                    advancement[team]["E8"] += 1

                # E8 winner
                advancement[results["E8"]]["FF"] += 1

            # FF winners
            for team in bracket["FF"]:
                advancement[team]["CG"] += 1

            # Champion
            advancement[bracket["Champion"]]["CHAMP"] += 1
            champions[bracket["Champion"]] += 1

        if verbose:
            print(f"Simulation complete!")
            print()

        return advancement, champions, all_brackets


# =============================================================================
# BRACKET GENERATOR
# =============================================================================

class BracketGenerator:
    """
    Generates 20 diverse brackets from Monte Carlo simulation results.

    Strategy for accuracy-focused brackets:
    - 7 brackets: Pick highest-probability winner every game ("chalk max")
    - 7 brackets: Probability-weighted random sampling (moderate diversity)
    - 6 brackets: Strategic upset injection (cover likely upset scenarios)
    """

    def __init__(self, simulator, calibration_scale):
        self.sim = simulator
        self.scale = calibration_scale

    def get_matchup_probability(self, team_a, team_b, round_name):
        """Get win probability for team_a vs team_b."""
        return predict_game(team_a, team_b, round_name, self.scale)

    def generate_chalk_bracket(self):
        """
        Generate the maximum-likelihood bracket.
        Always picks the higher-probability team.
        """
        bracket = {}
        region_champs = {}

        for region in self.sim.regions:
            matchups = BRACKET_MATCHUPS[region]
            results = {"R64": [], "R32": [], "S16": [], "E8": None}

            # R64
            r64 = []
            for team_a, team_b in matchups:
                prob_a = self.get_matchup_probability(team_a, team_b, "R64")
                winner = team_a if prob_a >= 0.5 else team_b
                r64.append(winner)
            results["R64"] = r64

            # R32
            r32 = []
            for i in range(0, 8, 2):
                prob_a = self.get_matchup_probability(r64[i], r64[i + 1], "R32")
                winner = r64[i] if prob_a >= 0.5 else r64[i + 1]
                r32.append(winner)
            results["R32"] = r32

            # S16
            s16 = []
            for i in range(0, 4, 2):
                prob_a = self.get_matchup_probability(r32[i], r32[i + 1], "S16")
                winner = r32[i] if prob_a >= 0.5 else r32[i + 1]
                s16.append(winner)
            results["S16"] = s16

            # E8
            prob_a = self.get_matchup_probability(s16[0], s16[1], "E8")
            e8_winner = s16[0] if prob_a >= 0.5 else s16[1]
            results["E8"] = e8_winner

            bracket[region] = results
            region_champs[region] = e8_winner

        # Final Four
        ff = []
        for region_a, region_b in self.sim.ff_matchups:
            prob_a = self.get_matchup_probability(
                region_champs[region_a], region_champs[region_b], "FF"
            )
            winner = region_champs[region_a] if prob_a >= 0.5 else region_champs[region_b]
            ff.append(winner)
        bracket["FF"] = ff

        # Championship
        prob_a = self.get_matchup_probability(ff[0], ff[1], "CG")
        bracket["Champion"] = ff[0] if prob_a >= 0.5 else ff[1]

        return bracket

    def generate_weighted_bracket(self, upset_bias=0.0):
        """
        Generate a bracket using probability-weighted random sampling.
        upset_bias: 0.0 = pure probability, positive = favor more upsets
        """
        bracket = {}
        region_champs = {}

        for region in self.sim.regions:
            matchups = BRACKET_MATCHUPS[region]
            results = {"R64": [], "R32": [], "S16": [], "E8": None}

            # R64
            r64 = []
            for team_a, team_b in matchups:
                prob_a = self.get_matchup_probability(team_a, team_b, "R64")
                # Apply upset bias
                if prob_a > 0.5:
                    prob_a = max(0.05, prob_a - upset_bias)
                else:
                    prob_a = min(0.95, prob_a + upset_bias)
                winner = team_a if random.random() < prob_a else team_b
                r64.append(winner)
            results["R64"] = r64

            # R32
            r32 = []
            for i in range(0, 8, 2):
                prob_a = self.get_matchup_probability(r64[i], r64[i + 1], "R32")
                if prob_a > 0.5:
                    prob_a = max(0.05, prob_a - upset_bias * 0.5)
                else:
                    prob_a = min(0.95, prob_a + upset_bias * 0.5)
                winner = r64[i] if random.random() < prob_a else r64[i + 1]
                r32.append(winner)
            results["R32"] = r32

            # S16
            s16 = []
            for i in range(0, 4, 2):
                prob_a = self.get_matchup_probability(r32[i], r32[i + 1], "S16")
                winner = r32[i] if random.random() < prob_a else r32[i + 1]
                s16.append(winner)
            results["S16"] = s16

            # E8
            prob_a = self.get_matchup_probability(s16[0], s16[1], "E8")
            e8_winner = s16[0] if random.random() < prob_a else s16[1]
            results["E8"] = e8_winner

            bracket[region] = results
            region_champs[region] = e8_winner

        # Final Four
        ff = []
        for region_a, region_b in self.sim.ff_matchups:
            prob_a = self.get_matchup_probability(
                region_champs[region_a], region_champs[region_b], "FF"
            )
            winner = region_champs[region_a] if random.random() < prob_a else region_champs[region_b]
            ff.append(winner)
        bracket["FF"] = ff

        # Championship
        prob_a = self.get_matchup_probability(ff[0], ff[1], "CG")
        bracket["Champion"] = ff[0] if random.random() < prob_a else ff[1]

        return bracket

    def generate_20_brackets(self, advancement_data, champion_counts, n_sims):
        """
        Generate 20 strategically diverse brackets.

        Distribution:
        - Brackets 1-3: Pure chalk (maximum likelihood)
          - 1 with most likely champion
          - 1 with 2nd most likely champion
          - 1 with 3rd most likely champion
        - Brackets 4-10: Moderate probability sampling (upset_bias=0.0)
          - Each seeded with a different top-7 champion
        - Brackets 11-16: Slight upset lean (upset_bias=0.03-0.06)
        - Brackets 17-20: Heavier upset lean (upset_bias=0.08-0.12)
        """
        brackets = []

        # Get top champions by frequency
        top_champs = champion_counts.most_common(10)
        print("\nTop 10 championship probabilities from simulation:")
        print("-" * 50)
        for team, count in top_champs:
            seed = TEAMS[team]["seed"]
            pct = count / n_sims * 100
            print(f"  ({seed}) {team}: {pct:.1f}%")
        print()

        # --- Brackets 1-3: Chalk brackets with top 3 champions ---
        print("Generating brackets 1-3: Chalk brackets...")
        for i in range(3):
            if i < len(top_champs):
                target_champ = top_champs[i][0]
                bracket = self._generate_bracket_with_champion(target_champ)
                bracket["_strategy"] = f"Chalk - {target_champ} champion"
                bracket["_number"] = i + 1
                brackets.append(bracket)

        # --- Brackets 4-10: Moderate diversity with specific champions ---
        print("Generating brackets 4-10: Moderate diversity...")
        for i in range(3, 10):
            champ_idx = i % len(top_champs)
            if champ_idx < len(top_champs):
                target_champ = top_champs[champ_idx][0]
            bracket = self.generate_weighted_bracket(upset_bias=0.0)
            # Force the champion to be from top champions for diversity
            # We regenerate until we get a bracket with this champion
            # (or accept after 50 tries to avoid infinite loops)
            for attempt in range(50):
                bracket = self.generate_weighted_bracket(upset_bias=0.0)
                if bracket["Champion"] == target_champ:
                    break
            bracket["_strategy"] = f"Moderate - {bracket['Champion']} champion"
            bracket["_number"] = i + 1
            brackets.append(bracket)

        # --- Brackets 11-16: Slight upset lean ---
        print("Generating brackets 11-16: Slight upset lean...")
        for i in range(10, 16):
            bias = 0.03 + (i - 10) * 0.006  # 0.03 to 0.06
            bracket = self.generate_weighted_bracket(upset_bias=bias)
            bracket["_strategy"] = f"Upset lean ({bias:.3f}) - {bracket['Champion']} champion"
            bracket["_number"] = i + 1
            brackets.append(bracket)

        # --- Brackets 17-20: Heavier upset lean ---
        print("Generating brackets 17-20: Heavy upset lean...")
        for i in range(16, 20):
            bias = 0.08 + (i - 16) * 0.015  # 0.08 to 0.125
            bracket = self.generate_weighted_bracket(upset_bias=bias)
            bracket["_strategy"] = f"Chaos ({bias:.3f}) - {bracket['Champion']} champion"
            bracket["_number"] = i + 1
            brackets.append(bracket)

        # Ensure champion diversity across all 20 brackets
        champ_distribution = Counter(b["Champion"] for b in brackets)
        print(f"\nChampion distribution across 20 brackets:")
        for team, count in champ_distribution.most_common():
            seed = TEAMS[team]["seed"]
            print(f"  ({seed}) {team}: {count} brackets")

        return brackets

    def _generate_bracket_with_champion(self, target_champion):
        """
        Generate a chalk-style bracket that results in target_champion winning.
        Picks highest-probability winner in every game, but ensures the
        target champion wins all their games.
        """
        bracket = {}
        region_champs = {}
        target_region = TEAMS[target_champion]["region"]

        for region in self.sim.regions:
            matchups = BRACKET_MATCHUPS[region]
            results = {"R64": [], "R32": [], "S16": [], "E8": None}

            # R64
            r64 = []
            for team_a, team_b in matchups:
                if region == target_region and (team_a == target_champion or team_b == target_champion):
                    winner = target_champion
                else:
                    prob_a = self.get_matchup_probability(team_a, team_b, "R64")
                    winner = team_a if prob_a >= 0.5 else team_b
                r64.append(winner)
            results["R64"] = r64

            # R32
            r32 = []
            for i in range(0, 8, 2):
                if region == target_region and (r64[i] == target_champion or r64[i+1] == target_champion):
                    winner = target_champion
                else:
                    prob_a = self.get_matchup_probability(r64[i], r64[i + 1], "R32")
                    winner = r64[i] if prob_a >= 0.5 else r64[i + 1]
                r32.append(winner)
            results["R32"] = r32

            # S16
            s16 = []
            for i in range(0, 4, 2):
                if region == target_region and (r32[i] == target_champion or r32[i+1] == target_champion):
                    winner = target_champion
                else:
                    prob_a = self.get_matchup_probability(r32[i], r32[i + 1], "S16")
                    winner = r32[i] if prob_a >= 0.5 else r32[i + 1]
                s16.append(winner)
            results["S16"] = s16

            # E8
            if region == target_region and (s16[0] == target_champion or s16[1] == target_champion):
                e8_winner = target_champion
            else:
                prob_a = self.get_matchup_probability(s16[0], s16[1], "E8")
                e8_winner = s16[0] if prob_a >= 0.5 else s16[1]
            results["E8"] = e8_winner

            bracket[region] = results
            region_champs[region] = e8_winner

        # Final Four — ensure target champion advances
        ff = []
        for region_a, region_b in self.sim.ff_matchups:
            champ_a = region_champs[region_a]
            champ_b = region_champs[region_b]
            if champ_a == target_champion or champ_b == target_champion:
                winner = target_champion
            else:
                prob_a = self.get_matchup_probability(champ_a, champ_b, "FF")
                winner = champ_a if prob_a >= 0.5 else champ_b
            ff.append(winner)
        bracket["FF"] = ff

        # Championship
        bracket["Champion"] = target_champion

        return bracket


# =============================================================================
# REPORTING
# =============================================================================

def print_advancement_table(advancement, n_sims, top_n=30):
    """Print a formatted advancement probability table."""
    rounds = ["R32", "S16", "E8", "FF", "CG", "CHAMP"]
    round_labels = ["Rd of 32", "Sweet 16", "Elite 8", "Final 4", "Title Game", "Champion"]

    # Sort teams by championship probability
    team_champ_probs = []
    for team in TEAMS:
        champ_count = advancement[team].get("CHAMP", 0)
        team_champ_probs.append((team, champ_count / n_sims))
    team_champ_probs.sort(key=lambda x: x[1], reverse=True)

    print()
    print("=" * 110)
    header = f"{'Team':<25} {'Seed':>4}"
    for label in round_labels:
        header += f" {label:>10}"
    print(header)
    print("=" * 110)

    for team, _ in team_champ_probs[:top_n]:
        seed = TEAMS[team]["seed"]
        region = TEAMS[team]["region"][0]  # First letter
        line = f"({seed:>2}) {team:<20} [{region}]"
        for r in rounds:
            count = advancement[team].get(r, 0)
            pct = count / n_sims * 100
            if pct >= 99.5:
                line += f" {'99.9%':>10}"
            elif pct < 0.1 and count > 0:
                line += f" {'<0.1%':>10}"
            elif count == 0:
                line += f" {'—':>10}"
            else:
                line += f" {pct:>9.1f}%"
        print(line)

    print("=" * 110)


def print_bracket(bracket, bracket_num=None):
    """Print a single bracket in readable format."""
    strategy = bracket.get("_strategy", "")
    num = bracket.get("_number", bracket_num)

    print()
    print(f"{'='*70}")
    if num:
        print(f"BRACKET #{num}: {strategy}")
    print(f"{'='*70}")

    regions = ["East", "West", "South", "Midwest"]
    round_names = ["R64", "R32", "S16", "E8"]
    round_labels = ["Round of 64", "Round of 32", "Sweet 16", "Elite 8"]

    for region in regions:
        print(f"\n--- {region.upper()} REGION ---")
        results = bracket[region]

        # R64
        matchups = BRACKET_MATCHUPS[region]
        print(f"  Round of 64:")
        for i, (team_a, team_b) in enumerate(matchups):
            winner = results["R64"][i]
            loser = team_b if winner == team_a else team_a
            seed_w = TEAMS[winner]["seed"]
            seed_l = TEAMS[loser]["seed"]
            upset = " *UPSET*" if seed_w > seed_l else ""
            print(f"    ({seed_w}) {winner} over ({seed_l}) {loser}{upset}")

        # R32
        print(f"  Round of 32:")
        for i, winner in enumerate(results["R32"]):
            j = i * 2
            loser = results["R64"][j] if results["R64"][j] != winner else results["R64"][j+1]
            seed_w = TEAMS[winner]["seed"]
            seed_l = TEAMS[loser]["seed"]
            upset = " *UPSET*" if seed_w > seed_l else ""
            print(f"    ({seed_w}) {winner} over ({seed_l}) {loser}{upset}")

        # S16
        print(f"  Sweet 16:")
        for i, winner in enumerate(results["S16"]):
            j = i * 2
            loser = results["R32"][j] if results["R32"][j] != winner else results["R32"][j+1]
            seed_w = TEAMS[winner]["seed"]
            seed_l = TEAMS[loser]["seed"]
            upset = " *UPSET*" if seed_w > seed_l else ""
            print(f"    ({seed_w}) {winner} over ({seed_l}) {loser}{upset}")

        # E8
        winner = results["E8"]
        loser = results["S16"][0] if results["S16"][0] != winner else results["S16"][1]
        seed_w = TEAMS[winner]["seed"]
        seed_l = TEAMS[loser]["seed"]
        upset = " *UPSET*" if seed_w > seed_l else ""
        print(f"  Elite 8:")
        print(f"    ({seed_w}) {winner} over ({seed_l}) {loser}{upset}")

    # Final Four
    print(f"\n--- FINAL FOUR ---")
    ff = bracket["FF"]
    ff_pairings = [("South", "East"), ("Midwest", "West")]
    for i, (r_a, r_b) in enumerate(ff_pairings):
        winner = ff[i]
        champ_a = bracket[r_a]["E8"]
        champ_b = bracket[r_b]["E8"]
        loser = champ_a if champ_a != winner else champ_b
        seed_w = TEAMS[winner]["seed"]
        seed_l = TEAMS[loser]["seed"]
        print(f"  ({seed_w}) {winner} over ({seed_l}) {loser}")

    # Championship
    print(f"\n--- CHAMPIONSHIP ---")
    champion = bracket["Champion"]
    loser = ff[0] if ff[0] != champion else ff[1]
    seed_w = TEAMS[champion]["seed"]
    seed_l = TEAMS[loser]["seed"]
    print(f"  CHAMPION: ({seed_w}) {champion} over ({seed_l}) {loser}")
    print(f"{'='*70}")


def count_upsets_in_bracket(bracket):
    """Count the number of upsets in a bracket."""
    upsets = 0
    for region in ["East", "West", "South", "Midwest"]:
        results = bracket[region]
        matchups = BRACKET_MATCHUPS[region]

        # R64
        for i, (team_a, team_b) in enumerate(matchups):
            winner = results["R64"][i]
            loser = team_b if winner == team_a else team_a
            if TEAMS[winner]["seed"] > TEAMS[loser]["seed"]:
                upsets += 1

        # R32
        for i, winner in enumerate(results["R32"]):
            j = i * 2
            loser = results["R64"][j] if results["R64"][j] != winner else results["R64"][j+1]
            if TEAMS[winner]["seed"] > TEAMS[loser]["seed"]:
                upsets += 1

        # S16
        for i, winner in enumerate(results["S16"]):
            j = i * 2
            loser = results["R32"][j] if results["R32"][j] != winner else results["R32"][j+1]
            if TEAMS[winner]["seed"] > TEAMS[loser]["seed"]:
                upsets += 1

        # E8
        winner = results["E8"]
        loser = results["S16"][0] if results["S16"][0] != winner else results["S16"][1]
        if TEAMS[winner]["seed"] > TEAMS[loser]["seed"]:
            upsets += 1

    return upsets
