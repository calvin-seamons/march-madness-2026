"""
2026 NCAA Tournament Team Data
All 68 teams with power ratings, stats, and metadata.
Sources: KenPom, NET, Vegas odds, ESPN, CBS Sports, SI
"""

# =============================================================================
# TEAM DATABASE
# Each team entry contains:
#   name, seed, region, kenpom_adj_em, net_rank, record_pct,
#   injury_factor (0=healthy, 1=devastating loss),
#   momentum (positive=hot, negative=cold),
#   coach_tourney_exp (number of tournament appearances),
#   tempo_rank (1=fastest, 362=slowest),
#   luck (KenPom luck rating, higher = more regression expected)
# =============================================================================

TEAMS = {
    # =========================================================================
    # EAST REGION (Regional: Washington D.C.)
    # =========================================================================
    "Duke": {
        "seed": 1, "region": "East",
        "kenpom_em": 39.65, "net_rank": 1,
        "record": "32-2", "record_pct": 0.941,
        "adj_o_rank": 4, "adj_d_rank": 2,
        "injury_factor": 0.15,  # Foster (foot) out, Ngongba questionable
        "momentum": 0.8,  # ACC champs
        "coach_tourney_exp": 15,  # Jon Scheyer inheriting Duke's machine
        "luck": 0.02,
        "fg_pct_3pt": 0.38, "opp_fg_pct_3pt": 0.28,
        "to_rate": 0.16, "oreb_pct": 0.32, "ft_pct": 0.74,
    },
    "Siena": {
        "seed": 16, "region": "East",
        "kenpom_em": -5.0, "net_rank": 180,
        "record": "23-11", "record_pct": 0.676,
        "adj_o_rank": 200, "adj_d_rank": 150,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 2,
        "luck": 0.04,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.19, "oreb_pct": 0.28, "ft_pct": 0.70,
    },
    "Ohio State": {
        "seed": 8, "region": "East",
        "kenpom_em": 14.5, "net_rank": 29,
        "record": "21-12", "record_pct": 0.636,
        "adj_o_rank": 40, "adj_d_rank": 35,
        "injury_factor": 0.0,
        "momentum": -0.2,
        "coach_tourney_exp": 5,
        "luck": 0.03,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.18, "oreb_pct": 0.30, "ft_pct": 0.72,
    },
    "TCU": {
        "seed": 9, "region": "East",
        "kenpom_em": 14.0, "net_rank": 39,
        "record": "22-11", "record_pct": 0.667,
        "adj_o_rank": 45, "adj_d_rank": 50,
        "injury_factor": 0.0,
        "momentum": 0.6,  # Won 9 of last 11
        "coach_tourney_exp": 4,
        "luck": 0.02,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.17, "oreb_pct": 0.29, "ft_pct": 0.71,
    },
    "St. John's": {
        "seed": 5, "region": "East",
        "kenpom_em": 21.0, "net_rank": 16,
        "record": "28-6", "record_pct": 0.824,
        "adj_o_rank": 25, "adj_d_rank": 12,
        "injury_factor": 0.0,
        "momentum": 0.9,  # 16-1 in last 17, Big East tourney champs
        "coach_tourney_exp": 8,
        "luck": 0.01,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.30,
        "to_rate": 0.125,  # Elite ball security
        "oreb_pct": 0.31, "ft_pct": 0.73,
    },
    "Northern Iowa": {
        "seed": 12, "region": "East",
        "kenpom_em": 8.5, "net_rank": 75,
        "record": "23-12", "record_pct": 0.657,
        "adj_o_rank": 90, "adj_d_rank": 65,
        "injury_factor": 0.0,
        "momentum": 0.5,  # MVC tourney champs
        "coach_tourney_exp": 6,
        "luck": 0.03,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.17, "oreb_pct": 0.30, "ft_pct": 0.71,
    },
    "Kansas": {
        "seed": 4, "region": "East",
        "kenpom_em": 19.5, "net_rank": 21,
        "record": "23-10", "record_pct": 0.697,
        "adj_o_rank": 100, "adj_d_rank": 38,
        "injury_factor": 0.2,  # Peterson inconsistent health
        "momentum": -0.4,  # 3-4 in final 7
        "coach_tourney_exp": 20,  # Bill Self - elite
        "luck": 0.04,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.32,
        "to_rate": 0.18, "oreb_pct": 0.31, "ft_pct": 0.70,
    },
    "Cal Baptist": {
        "seed": 13, "region": "East",
        "kenpom_em": 4.0, "net_rank": 110,
        "record": "25-8", "record_pct": 0.758,
        "adj_o_rank": 120, "adj_d_rank": 100,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 2,
        "luck": 0.03,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.18, "oreb_pct": 0.29, "ft_pct": 0.70,
    },
    "Louisville": {
        "seed": 6, "region": "East",
        "kenpom_em": 18.0, "net_rank": 17,
        "record": "23-10", "record_pct": 0.697,
        "adj_o_rank": 30, "adj_d_rank": 25,
        "injury_factor": 0.1,  # Mikel Brown sore back
        "momentum": 0.3,
        "coach_tourney_exp": 10,
        "luck": 0.02,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.32,
        "to_rate": 0.17, "oreb_pct": 0.31, "ft_pct": 0.72,
    },
    "South Florida": {
        "seed": 11, "region": "East",
        "kenpom_em": 13.0, "net_rank": 45,
        "record": "25-8", "record_pct": 0.758,  # Corrected from 24-8
        "adj_o_rank": 55, "adj_d_rank": 40,
        "injury_factor": 0.0,
        "momentum": 0.7,  # American champs, 3 losses in last 22 all by 1-3 pts
        "coach_tourney_exp": 3,
        "luck": -0.02,  # Unlucky — close losses
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.32,
        "to_rate": 0.17, "oreb_pct": 0.30, "ft_pct": 0.71,
    },
    "Michigan State": {
        "seed": 3, "region": "East",
        "kenpom_em": 24.0, "net_rank": 11,
        "record": "25-7", "record_pct": 0.781,
        "adj_o_rank": 20, "adj_d_rank": 8,
        "injury_factor": 0.0,
        "momentum": 0.5,
        "coach_tourney_exp": 25,  # Tom Izzo — March legend
        "luck": 0.01,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.31,
        "to_rate": 0.17, "oreb_pct": 0.34,  # 7th nationally in OREB
        "ft_pct": 0.72,
    },
    "North Dakota State": {
        "seed": 14, "region": "East",
        "kenpom_em": 2.0, "net_rank": 130,
        "record": "27-7", "record_pct": 0.794,
        "adj_o_rank": 100, "adj_d_rank": 140,
        "injury_factor": 0.0,
        "momentum": 0.4,
        "coach_tourney_exp": 4,
        "luck": 0.02,
        "fg_pct_3pt": 0.37,  # Five players shooting 36%+ on 100+ attempts
        "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.18, "oreb_pct": 0.28, "ft_pct": 0.71,
    },
    "UCLA": {
        "seed": 7, "region": "East",
        "kenpom_em": 16.0, "net_rank": 30,
        "record": "23-11", "record_pct": 0.676,
        "adj_o_rank": 35, "adj_d_rank": 30,
        "injury_factor": 0.15,  # Dent calf strain, Bilodeau knee questionable
        "momentum": 0.5,  # Late season surge, beat MSU
        "coach_tourney_exp": 8,
        "luck": 0.03,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.17, "oreb_pct": 0.30, "ft_pct": 0.71,
    },
    "UCF": {
        "seed": 10, "region": "East",
        "kenpom_em": 12.0, "net_rank": 51,
        "record": "21-11", "record_pct": 0.656,
        "adj_o_rank": 60, "adj_d_rank": 55,
        "injury_factor": 0.0,
        "momentum": 0.2,
        "coach_tourney_exp": 3,
        "luck": 0.02,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.18, "oreb_pct": 0.29, "ft_pct": 0.70,
    },
    "UConn": {
        "seed": 2, "region": "East",
        "kenpom_em": 26.0, "net_rank": 10,
        "record": "29-5", "record_pct": 0.853,
        "adj_o_rank": 15, "adj_d_rank": 10,
        "injury_factor": 0.1,  # Demary ankle questionable
        "momentum": -0.7,  # Lost finale, blown out 72-52 in Big East final
        "coach_tourney_exp": 12,  # Dan Hurley
        "luck": 0.05,
        "fg_pct_3pt": 0.33, "opp_fg_pct_3pt": 0.30,
        "to_rate": 0.19,  # 16 turnovers in Big East final
        "oreb_pct": 0.33, "ft_pct": 0.72,
    },
    "Furman": {
        "seed": 15, "region": "East",
        "kenpom_em": -1.0, "net_rank": 150,
        "record": "22-12", "record_pct": 0.647,
        "adj_o_rank": 140, "adj_d_rank": 130,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 3,
        "luck": 0.02,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.18, "oreb_pct": 0.28, "ft_pct": 0.70,
    },

    # =========================================================================
    # WEST REGION (Regional: San Jose, CA)
    # =========================================================================
    "Arizona": {
        "seed": 1, "region": "West",
        "kenpom_em": 37.7, "net_rank": 3,
        "record": "32-2", "record_pct": 0.941,
        "adj_o_rank": 5, "adj_d_rank": 3,
        "injury_factor": 0.0,  # Healthiest of top teams
        "momentum": 0.8,  # Big 12 champs
        "coach_tourney_exp": 8,  # Tommy Lloyd
        "luck": 0.01,
        "fg_pct_3pt": 0.37, "opp_fg_pct_3pt": 0.29,
        "to_rate": 0.16, "oreb_pct": 0.35,  # +9.44 rebound margin in Big 12
        "ft_pct": 0.73,
    },
    "Long Island": {
        "seed": 16, "region": "West",
        "kenpom_em": -8.0, "net_rank": 220,
        "record": "24-10", "record_pct": 0.706,
        "adj_o_rank": 230, "adj_d_rank": 180,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 1,
        "luck": 0.04,
        "fg_pct_3pt": 0.33, "opp_fg_pct_3pt": 0.35,
        "to_rate": 0.20, "oreb_pct": 0.27, "ft_pct": 0.69,
    },
    "Villanova": {
        "seed": 8, "region": "West",
        "kenpom_em": 14.0, "net_rank": 35,
        "record": "24-8", "record_pct": 0.750,
        "adj_o_rank": 42, "adj_d_rank": 38,
        "injury_factor": 0.15,  # Hodge torn ACL
        "momentum": 0.2,
        "coach_tourney_exp": 12,
        "luck": 0.02,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.17, "oreb_pct": 0.29, "ft_pct": 0.73,
    },
    "Utah State": {
        "seed": 9, "region": "West",
        "kenpom_em": 15.0, "net_rank": 26,
        "record": "28-6", "record_pct": 0.824,
        "adj_o_rank": 35, "adj_d_rank": 30,
        "injury_factor": 0.0,
        "momentum": 0.5,
        "coach_tourney_exp": 5,
        "luck": 0.01,
        "fg_pct_3pt": 0.36, "opp_fg_pct_3pt": 0.32,
        "to_rate": 0.16, "oreb_pct": 0.31, "ft_pct": 0.72,
    },
    "Wisconsin": {
        "seed": 5, "region": "West",
        "kenpom_em": 18.5, "net_rank": 25,
        "record": "24-10", "record_pct": 0.706,
        "adj_o_rank": 28, "adj_d_rank": 22,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 10,
        "luck": 0.02,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.32,
        "to_rate": 0.16, "oreb_pct": 0.29, "ft_pct": 0.73,
    },
    "High Point": {
        "seed": 12, "region": "West",
        "kenpom_em": 7.0, "net_rank": 85,
        "record": "30-4", "record_pct": 0.882,
        "adj_o_rank": 30, "adj_d_rank": 120,
        "injury_factor": 0.0,
        "momentum": 0.6,
        "coach_tourney_exp": 1,
        "luck": 0.03,
        "fg_pct_3pt": 0.37, "opp_fg_pct_3pt": 0.35,
        "to_rate": 0.17, "oreb_pct": 0.30, "ft_pct": 0.72,
    },
    "Arkansas": {
        "seed": 4, "region": "West",
        "kenpom_em": 22.0, "net_rank": 15,
        "record": "26-8", "record_pct": 0.765,
        "adj_o_rank": 18, "adj_d_rank": 15,
        "injury_factor": 0.0,
        "momentum": 0.8,  # SEC tourney champs
        "coach_tourney_exp": 20,  # John Calipari
        "luck": 0.01,
        "fg_pct_3pt": 0.36, "opp_fg_pct_3pt": 0.31,
        "to_rate": 0.16, "oreb_pct": 0.32, "ft_pct": 0.72,
    },
    "Hawaii": {
        "seed": 13, "region": "West",
        "kenpom_em": 3.0, "net_rank": 120,
        "record": "24-8", "record_pct": 0.750,
        "adj_o_rank": 130, "adj_d_rank": 110,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 2,
        "luck": 0.03,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.18, "oreb_pct": 0.28, "ft_pct": 0.70,
    },
    "BYU": {
        "seed": 6, "region": "West",
        "kenpom_em": 17.0, "net_rank": 23,
        "record": "23-11", "record_pct": 0.676,
        "adj_o_rank": 22, "adj_d_rank": 28,
        "injury_factor": 0.35,  # Saunders torn ACL — 18 PPG, 38% from 3
        "momentum": -0.5,  # Lost 4 of final 6
        "coach_tourney_exp": 5,
        "luck": 0.04,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.17, "oreb_pct": 0.29, "ft_pct": 0.71,
    },
    # First Four winner placeholder — will be Texas or NC State
    "Texas/NC State": {
        "seed": 11, "region": "West",
        "kenpom_em": 11.5, "net_rank": 38,
        "record": "19-14", "record_pct": 0.576,
        "adj_o_rank": 50, "adj_d_rank": 45,
        "injury_factor": 0.0,
        "momentum": 0.2,
        "coach_tourney_exp": 8,
        "luck": 0.03,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.18, "oreb_pct": 0.29, "ft_pct": 0.71,
    },
    "Gonzaga": {
        "seed": 3, "region": "West",
        "kenpom_em": 23.0, "net_rank": 7,
        "record": "30-3", "record_pct": 0.909,
        "adj_o_rank": 14, "adj_d_rank": 8,
        "injury_factor": 0.3,  # Braden Huff out (17.8 PPG) — offense 14th→68th
        "momentum": 0.4,  # WCC champs
        "coach_tourney_exp": 15,  # Mark Few
        "luck": 0.02,
        "fg_pct_3pt": 0.36, "opp_fg_pct_3pt": 0.30,
        "to_rate": 0.16, "oreb_pct": 0.32, "ft_pct": 0.74,
    },
    "Kennesaw State": {
        "seed": 14, "region": "West",
        "kenpom_em": 0.5, "net_rank": 145,
        "record": "21-13", "record_pct": 0.618,
        "adj_o_rank": 150, "adj_d_rank": 135,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 2,
        "luck": 0.03,
        "fg_pct_3pt": 0.33, "opp_fg_pct_3pt": 0.35,
        "to_rate": 0.19, "oreb_pct": 0.28, "ft_pct": 0.69,
    },
    "Miami FL": {
        "seed": 7, "region": "West",
        "kenpom_em": 15.5, "net_rank": 32,
        "record": "25-8", "record_pct": 0.758,
        "adj_o_rank": 38, "adj_d_rank": 32,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 10,
        "luck": 0.02,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.17, "oreb_pct": 0.30, "ft_pct": 0.72,
    },
    "Missouri": {
        "seed": 10, "region": "West",
        "kenpom_em": 11.0, "net_rank": 58,
        "record": "20-12", "record_pct": 0.625,
        "adj_o_rank": 65, "adj_d_rank": 55,
        "injury_factor": 0.0,
        "momentum": 0.1,
        "coach_tourney_exp": 5,
        "luck": 0.03,
        "fg_pct_3pt": 0.33, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.18, "oreb_pct": 0.29, "ft_pct": 0.70,
    },
    "Purdue": {
        "seed": 2, "region": "West",
        "kenpom_em": 25.5, "net_rank": 9,
        "record": "27-8", "record_pct": 0.771,
        "adj_o_rank": 3, "adj_d_rank": 88,  # Defensive regression
        "injury_factor": 0.0,
        "momentum": 0.6,  # Big Ten tourney champs — rebounded
        "coach_tourney_exp": 12,  # Matt Painter
        "luck": 0.04,
        "fg_pct_3pt": 0.36, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.16, "oreb_pct": 0.31, "ft_pct": 0.74,
    },
    "Queens": {
        "seed": 15, "region": "West",
        "kenpom_em": -2.0, "net_rank": 160,
        "record": "21-13", "record_pct": 0.618,
        "adj_o_rank": 155, "adj_d_rank": 145,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 1,
        "luck": 0.03,
        "fg_pct_3pt": 0.33, "opp_fg_pct_3pt": 0.35,
        "to_rate": 0.19, "oreb_pct": 0.27, "ft_pct": 0.69,
    },

    # =========================================================================
    # SOUTH REGION (Regional: Houston, TX)
    # =========================================================================
    "Florida": {
        "seed": 1, "region": "South",
        "kenpom_em": 30.0, "net_rank": 4,
        "record": "26-7", "record_pct": 0.788,
        "adj_o_rank": 9, "adj_d_rank": 6,
        "injury_factor": 0.0,
        "momentum": 0.9,  # 11-game win streak, defending champs
        "coach_tourney_exp": 8,  # Todd Golden
        "luck": 0.01,
        "fg_pct_3pt": 0.36, "opp_fg_pct_3pt": 0.30,
        "to_rate": 0.16, "oreb_pct": 0.38,  # +14.5 rebound margin (nation's best)
        "ft_pct": 0.73,
    },
    "Prairie View/Lehigh": {
        "seed": 16, "region": "South",
        "kenpom_em": -10.0, "net_rank": 250,
        "record": "18-17", "record_pct": 0.514,
        "adj_o_rank": 260, "adj_d_rank": 220,
        "injury_factor": 0.0,
        "momentum": 0.2,
        "coach_tourney_exp": 1,
        "luck": 0.04,
        "fg_pct_3pt": 0.31, "opp_fg_pct_3pt": 0.36,
        "to_rate": 0.21, "oreb_pct": 0.26, "ft_pct": 0.67,
    },
    "Clemson": {
        "seed": 8, "region": "South",
        "kenpom_em": 13.5, "net_rank": 34,
        "record": "24-10", "record_pct": 0.706,
        "adj_o_rank": 50, "adj_d_rank": 35,
        "injury_factor": 0.2,  # Welling torn ACL
        "momentum": -0.2,
        "coach_tourney_exp": 6,
        "luck": 0.03,
        "fg_pct_3pt": 0.33, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.18, "oreb_pct": 0.29, "ft_pct": 0.70,
    },
    "Iowa": {
        "seed": 9, "region": "South",
        "kenpom_em": 14.5, "net_rank": 27,
        "record": "21-12", "record_pct": 0.636,
        "adj_o_rank": 25, "adj_d_rank": 45,
        "injury_factor": 0.0,
        "momentum": -0.6,  # Lost 7 of final 10
        "coach_tourney_exp": 8,
        "luck": 0.05,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.17, "oreb_pct": 0.30, "ft_pct": 0.72,
    },
    "Vanderbilt": {
        "seed": 5, "region": "South",
        "kenpom_em": 20.5, "net_rank": 13,
        "record": "26-8", "record_pct": 0.765,
        "adj_o_rank": 10, "adj_d_rank": 95,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 4,
        "luck": 0.02,
        "fg_pct_3pt": 0.36, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.16, "oreb_pct": 0.31, "ft_pct": 0.73,
    },
    "McNeese": {
        "seed": 12, "region": "South",
        "kenpom_em": 9.0, "net_rank": 56,
        "record": "28-5", "record_pct": 0.848,
        "adj_o_rank": 45, "adj_d_rank": 70,
        "injury_factor": 0.0,
        "momentum": 0.8,  # 10-game win streak, 3rd straight tourney
        "coach_tourney_exp": 3,
        "luck": 0.01,
        "fg_pct_3pt": 0.36, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.16, "oreb_pct": 0.31, "ft_pct": 0.72,
    },
    "Nebraska": {
        "seed": 4, "region": "South",
        "kenpom_em": 21.5, "net_rank": 14,
        "record": "26-6", "record_pct": 0.813,
        "adj_o_rank": 30, "adj_d_rank": 17,
        "injury_factor": 0.0,
        "momentum": 0.4,
        "coach_tourney_exp": 3,
        "luck": 0.01,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.30,  # Opponents shot 30% from 3
        "to_rate": 0.16, "oreb_pct": 0.31, "ft_pct": 0.72,
    },
    "Troy": {
        "seed": 13, "region": "South",
        "kenpom_em": 2.5, "net_rank": 135,
        "record": "22-11", "record_pct": 0.667,
        "adj_o_rank": 140, "adj_d_rank": 120,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 2,
        "luck": 0.03,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.19, "oreb_pct": 0.28, "ft_pct": 0.70,
    },
    "North Carolina": {
        "seed": 6, "region": "South",
        "kenpom_em": 17.5, "net_rank": 24,
        "record": "24-8", "record_pct": 0.750,
        "adj_o_rank": 20, "adj_d_rank": 35,
        "injury_factor": 0.4,  # Caleb Wilson OUT — expected top-5 NBA pick, 0-2 without
        "momentum": -0.5,
        "coach_tourney_exp": 12,  # Hubert Davis
        "luck": 0.04,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.17, "oreb_pct": 0.32, "ft_pct": 0.72,
    },
    "VCU": {
        "seed": 11, "region": "South",
        "kenpom_em": 14.5, "net_rank": 43,
        "record": "27-7", "record_pct": 0.794,  # Corrected from 26-7
        "adj_o_rank": 40, "adj_d_rank": 42,
        "injury_factor": 0.0,
        "momentum": 0.5,
        "coach_tourney_exp": 6,
        "luck": 0.01,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.32,
        "to_rate": 0.17, "oreb_pct": 0.31, "ft_pct": 0.72,
    },
    "Illinois": {
        "seed": 3, "region": "South",
        "kenpom_em": 25.0, "net_rank": 8,
        "record": "24-8", "record_pct": 0.750,
        "adj_o_rank": 1, "adj_d_rank": 41,
        "injury_factor": 0.0,
        "momentum": 0.4,
        "coach_tourney_exp": 6,
        "luck": 0.02,
        "fg_pct_3pt": 0.37, "opp_fg_pct_3pt": 0.32,
        "to_rate": 0.15, "oreb_pct": 0.32, "ft_pct": 0.74,
    },
    "Penn": {
        "seed": 14, "region": "South",
        "kenpom_em": -3.0, "net_rank": 170,
        "record": "18-11", "record_pct": 0.621,
        "adj_o_rank": 110, "adj_d_rank": 200,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 2,
        "luck": 0.03,
        "fg_pct_3pt": 0.386,  # Among best nationally
        "opp_fg_pct_3pt": 0.36,
        "to_rate": 0.17, "oreb_pct": 0.27, "ft_pct": 0.72,
    },
    "Saint Mary's": {
        "seed": 7, "region": "South",
        "kenpom_em": 16.5, "net_rank": 22,
        "record": "27-5", "record_pct": 0.844,
        "adj_o_rank": 109, "adj_d_rank": 18,
        "injury_factor": 0.0,
        "momentum": 0.4,
        "coach_tourney_exp": 10,  # Randy Bennett
        "luck": 0.02,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.30,
        "to_rate": 0.16, "oreb_pct": 0.30, "ft_pct": 0.73,
    },
    "Texas A&M": {
        "seed": 10, "region": "South",
        "kenpom_em": 13.0, "net_rank": 44,
        "record": "21-11", "record_pct": 0.656,
        "adj_o_rank": 55, "adj_d_rank": 45,
        "injury_factor": 0.0,
        "momentum": 0.2,
        "coach_tourney_exp": 8,
        "luck": 0.03,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.18, "oreb_pct": 0.30, "ft_pct": 0.71,
    },
    "Houston": {
        "seed": 2, "region": "South",
        "kenpom_em": 27.0, "net_rank": 5,
        "record": "28-6", "record_pct": 0.824,
        "adj_o_rank": 14, "adj_d_rank": 5,
        "injury_factor": 0.0,
        "momentum": 0.5,
        "coach_tourney_exp": 10,  # Kelvin Sampson
        "luck": 0.01,
        "fg_pct_3pt": 0.345, "opp_fg_pct_3pt": 0.29,
        "to_rate": 0.15,  # 3rd-best turnover rate nationally
        "oreb_pct": 0.33, "ft_pct": 0.72,
    },
    "Idaho": {
        "seed": 15, "region": "South",
        "kenpom_em": -3.5, "net_rank": 175,
        "record": "21-14", "record_pct": 0.600,
        "adj_o_rank": 160, "adj_d_rank": 155,
        "injury_factor": 0.0,
        "momentum": 0.2,
        "coach_tourney_exp": 1,
        "luck": 0.04,
        "fg_pct_3pt": 0.33, "opp_fg_pct_3pt": 0.35,
        "to_rate": 0.19, "oreb_pct": 0.27, "ft_pct": 0.69,
    },

    # =========================================================================
    # MIDWEST REGION (Regional: Chicago, IL)
    # =========================================================================
    "Michigan": {
        "seed": 1, "region": "Midwest",
        "kenpom_em": 39.43, "net_rank": 2,
        "record": "31-3", "record_pct": 0.912,
        "adj_o_rank": 5, "adj_d_rank": 1,  # No. 1 defense nationally (87.1)
        "injury_factor": 0.08,  # Cason torn ACL — backup guard
        "momentum": 0.6,
        "coach_tourney_exp": 6,
        "luck": 0.01,
        "fg_pct_3pt": 0.37, "opp_fg_pct_3pt": 0.28,
        "to_rate": 0.15, "oreb_pct": 0.34, "ft_pct": 0.74,
    },
    "UMBC/Howard": {
        "seed": 16, "region": "Midwest",
        "kenpom_em": -6.0, "net_rank": 200,
        "record": "24-9", "record_pct": 0.727,
        "adj_o_rank": 210, "adj_d_rank": 170,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 2,
        "luck": 0.04,
        "fg_pct_3pt": 0.33, "opp_fg_pct_3pt": 0.35,
        "to_rate": 0.20, "oreb_pct": 0.27, "ft_pct": 0.69,
    },
    "Georgia": {
        "seed": 8, "region": "Midwest",
        "kenpom_em": 13.5, "net_rank": 33,
        "record": "22-10", "record_pct": 0.688,
        "adj_o_rank": 45, "adj_d_rank": 40,
        "injury_factor": 0.0,
        "momentum": 0.2,
        "coach_tourney_exp": 4,
        "luck": 0.03,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.18, "oreb_pct": 0.30, "ft_pct": 0.71,
    },
    "Saint Louis": {
        "seed": 9, "region": "Midwest",
        "kenpom_em": 14.0, "net_rank": 31,
        "record": "28-5", "record_pct": 0.848,
        "adj_o_rank": 40, "adj_d_rank": 38,
        "injury_factor": 0.0,
        "momentum": 0.5,
        "coach_tourney_exp": 5,
        "luck": 0.02,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.32,
        "to_rate": 0.17, "oreb_pct": 0.30, "ft_pct": 0.72,
    },
    "Texas Tech": {
        "seed": 5, "region": "Midwest",
        "kenpom_em": 16.0, "net_rank": 19,
        "record": "22-10", "record_pct": 0.688,
        "adj_o_rank": 50, "adj_d_rank": 119,  # Fell from 24th post-Toppin
        "injury_factor": 0.5,  # Toppin torn ACL — All-American, 21.8 PPG/10.8 RPG
        "momentum": -0.3,  # 3-3 post-Toppin
        "coach_tourney_exp": 8,
        "luck": 0.04,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.17, "oreb_pct": 0.30, "ft_pct": 0.71,
    },
    "Akron": {
        "seed": 12, "region": "Midwest",
        "kenpom_em": 10.0, "net_rank": 54,
        "record": "29-5", "record_pct": 0.853,
        "adj_o_rank": 25, "adj_d_rank": 65,
        "injury_factor": 0.0,
        "momentum": 0.7,  # 17-1 in MAC, 3 straight tourney appearances
        "coach_tourney_exp": 3,
        "luck": 0.01,
        "fg_pct_3pt": 0.379, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.16, "oreb_pct": 0.31, "ft_pct": 0.72,
    },
    "Alabama": {
        "seed": 4, "region": "Midwest",
        "kenpom_em": 20.0, "net_rank": 18,
        "record": "23-9", "record_pct": 0.719,
        "adj_o_rank": 8, "adj_d_rank": 55,
        "injury_factor": 0.05,  # Holloway marijuana arrest — distraction
        "momentum": 0.7,  # Won 9 of final 10
        "coach_tourney_exp": 8,  # Nate Oats
        "luck": 0.03,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.18, "oreb_pct": 0.32, "ft_pct": 0.71,
    },
    "Hofstra": {
        "seed": 13, "region": "Midwest",
        "kenpom_em": 3.5, "net_rank": 115,
        "record": "24-10", "record_pct": 0.706,
        "adj_o_rank": 110, "adj_d_rank": 105,
        "injury_factor": 0.0,
        "momentum": 0.6,  # Dramatic CAA tourney run
        "coach_tourney_exp": 2,
        "luck": 0.03,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.18, "oreb_pct": 0.29, "ft_pct": 0.71,
    },
    "Tennessee": {
        "seed": 6, "region": "Midwest",
        "kenpom_em": 18.0, "net_rank": 20,
        "record": "22-11", "record_pct": 0.667,
        "adj_o_rank": 173, "adj_d_rank": 39,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 12,  # Rick Barnes
        "luck": 0.04,
        "fg_pct_3pt": 0.30,  # Terrible shooting
        "opp_fg_pct_3pt": 0.31,
        "to_rate": 0.17, "oreb_pct": 0.36,  # No. 1 OREB nationally
        "ft_pct": 0.70,
    },
    # First Four winner placeholder — Miami OH or SMU
    "Miami OH/SMU": {
        "seed": 11, "region": "Midwest",
        "kenpom_em": 12.0, "net_rank": 42,
        "record": "25-7", "record_pct": 0.781,
        "adj_o_rank": 55, "adj_d_rank": 48,
        "injury_factor": 0.0,
        "momentum": 0.4,
        "coach_tourney_exp": 4,
        "luck": 0.02,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.33,
        "to_rate": 0.17, "oreb_pct": 0.29, "ft_pct": 0.71,
    },
    "Virginia": {
        "seed": 3, "region": "Midwest",
        "kenpom_em": 23.5, "net_rank": 12,
        "record": "29-5", "record_pct": 0.853,
        "adj_o_rank": 25, "adj_d_rank": 7,
        "injury_factor": 0.0,
        "momentum": 0.7,  # 11-1 in final 12
        "coach_tourney_exp": 5,  # Ryan Odom
        "luck": 0.01,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.30,
        "to_rate": 0.16, "oreb_pct": 0.33,  # Top-6 OREB rate
        "ft_pct": 0.73,
    },
    "Wright State": {
        "seed": 14, "region": "Midwest",
        "kenpom_em": 1.0, "net_rank": 140,
        "record": "23-11", "record_pct": 0.676,
        "adj_o_rank": 135, "adj_d_rank": 125,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 3,
        "luck": 0.03,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.18, "oreb_pct": 0.28, "ft_pct": 0.70,
    },
    "Kentucky": {
        "seed": 7, "region": "Midwest",
        "kenpom_em": 15.0, "net_rank": 28,
        "record": "21-13", "record_pct": 0.618,
        "adj_o_rank": 35, "adj_d_rank": 40,
        "injury_factor": 0.3,  # Quaintance barely played all year
        "momentum": -0.5,  # Lost 5 of final 7
        "coach_tourney_exp": 15,  # Mark Pope
        "luck": 0.06,
        "fg_pct_3pt": 0.34, "opp_fg_pct_3pt": 0.34,
        "to_rate": 0.18, "oreb_pct": 0.29, "ft_pct": 0.71,
    },
    "Santa Clara": {
        "seed": 10, "region": "Midwest",
        "kenpom_em": 13.5, "net_rank": 40,
        "record": "26-8", "record_pct": 0.765,
        "adj_o_rank": 45, "adj_d_rank": 42,
        "injury_factor": 0.0,
        "momentum": 0.4,
        "coach_tourney_exp": 3,
        "luck": 0.02,
        "fg_pct_3pt": 0.36, "opp_fg_pct_3pt": 0.32,
        "to_rate": 0.17, "oreb_pct": 0.30, "ft_pct": 0.72,
    },
    "Iowa State": {
        "seed": 2, "region": "Midwest",
        "kenpom_em": 26.5, "net_rank": 6,
        "record": "27-7", "record_pct": 0.794,
        "adj_o_rank": 84, "adj_d_rank": 4,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 8,  # T.J. Otzelberger
        "luck": 0.02,
        "fg_pct_3pt": 0.35, "opp_fg_pct_3pt": 0.29,
        "to_rate": 0.15, "oreb_pct": 0.31, "ft_pct": 0.73,
    },
    "Tennessee State": {
        "seed": 15, "region": "Midwest",
        "kenpom_em": -2.5, "net_rank": 165,
        "record": "23-9", "record_pct": 0.719,
        "adj_o_rank": 150, "adj_d_rank": 140,
        "injury_factor": 0.0,
        "momentum": 0.3,
        "coach_tourney_exp": 1,
        "luck": 0.03,
        "fg_pct_3pt": 0.33, "opp_fg_pct_3pt": 0.35,
        "to_rate": 0.19, "oreb_pct": 0.28, "ft_pct": 0.70,
    },
}


# =============================================================================
# BRACKET STRUCTURE
# Defines the matchups in order: (team_a_seed, team_b_seed) within each region
# Standard bracket order: 1v16, 8v9, 5v12, 4v13, 6v11, 3v14, 7v10, 2v15
# =============================================================================

BRACKET_MATCHUPS = {
    "East": [
        ("Duke", "Siena"),                    # 1 vs 16
        ("Ohio State", "TCU"),                # 8 vs 9
        ("St. John's", "Northern Iowa"),      # 5 vs 12
        ("Kansas", "Cal Baptist"),            # 4 vs 13
        ("Louisville", "South Florida"),      # 6 vs 11
        ("Michigan State", "North Dakota State"),  # 3 vs 14
        ("UCLA", "UCF"),                      # 7 vs 10
        ("UConn", "Furman"),                  # 2 vs 15
    ],
    "West": [
        ("Arizona", "Long Island"),           # 1 vs 16
        ("Villanova", "Utah State"),          # 8 vs 9
        ("Wisconsin", "High Point"),          # 5 vs 12
        ("Arkansas", "Hawaii"),               # 4 vs 13
        ("BYU", "Texas/NC State"),            # 6 vs 11
        ("Gonzaga", "Kennesaw State"),        # 3 vs 14
        ("Miami FL", "Missouri"),             # 7 vs 10
        ("Purdue", "Queens"),                 # 2 vs 15
    ],
    "South": [
        ("Florida", "Prairie View/Lehigh"),   # 1 vs 16
        ("Clemson", "Iowa"),                  # 8 vs 9
        ("Vanderbilt", "McNeese"),            # 5 vs 12
        ("Nebraska", "Troy"),                 # 4 vs 13
        ("North Carolina", "VCU"),            # 6 vs 11
        ("Illinois", "Penn"),                 # 3 vs 14
        ("Saint Mary's", "Texas A&M"),        # 7 vs 10
        ("Houston", "Idaho"),                 # 2 vs 15
    ],
    "Midwest": [
        ("Michigan", "UMBC/Howard"),          # 1 vs 16
        ("Georgia", "Saint Louis"),           # 8 vs 9
        ("Texas Tech", "Akron"),              # 5 vs 12
        ("Alabama", "Hofstra"),               # 4 vs 13
        ("Tennessee", "Miami OH/SMU"),        # 6 vs 11
        ("Virginia", "Wright State"),         # 3 vs 14
        ("Kentucky", "Santa Clara"),          # 7 vs 10
        ("Iowa State", "Tennessee State"),    # 2 vs 15
    ],
}

# Second round matchups connect: game 0 winner vs game 1 winner, game 2 vs 3, etc.
# Sweet 16: R32 game 0-1 winner vs R32 game 2-3 winner, etc.
# Elite 8: S16 game 0 winner vs S16 game 1 winner
# Final Four: South champ vs East champ, Midwest champ vs West champ
# Note: The actual FF matchups depend on the bracket structure — using standard pairing


# =============================================================================
# VEGAS IMPLIED PROBABILITIES (vig-removed) for Round of 64
# These are our calibration targets
# =============================================================================

VEGAS_ODDS_R64 = {
    # East Region
    ("Duke", "Siena"): (0.995, 0.005),
    ("Ohio State", "TCU"): (0.543, 0.457),
    ("St. John's", "Northern Iowa"): (0.807, 0.193),
    ("Kansas", "Cal Baptist"): (0.843, 0.157),
    ("Louisville", "South Florida"): (0.686, 0.314),
    ("Michigan State", "North Dakota State"): (0.941, 0.059),
    ("UCLA", "UCF"): (0.710, 0.290),
    ("UConn", "Furman"): (0.978, 0.022),
    # West Region
    ("Arizona", "Long Island"): (0.995, 0.005),
    ("Villanova", "Utah State"): (0.458, 0.542),  # Utah State favored
    ("Wisconsin", "High Point"): (0.829, 0.171),
    ("Arkansas", "Hawaii"): (0.950, 0.050),
    ("BYU", "Texas/NC State"): (0.65, 0.35),  # Estimated
    ("Gonzaga", "Kennesaw State"): (0.970, 0.030),
    ("Miami FL", "Missouri"): (0.542, 0.458),
    ("Purdue", "Queens"): (0.978, 0.022),
    # South Region
    ("Florida", "Prairie View/Lehigh"): (0.995, 0.005),
    ("Clemson", "Iowa"): (0.435, 0.565),  # Iowa favored
    ("Vanderbilt", "McNeese"): (0.846, 0.154),
    ("Nebraska", "Troy"): (0.931, 0.069),
    ("North Carolina", "VCU"): (0.542, 0.458),
    ("Illinois", "Penn"): (0.985, 0.015),
    ("Saint Mary's", "Texas A&M"): (0.570, 0.430),
    ("Houston", "Idaho"): (0.978, 0.022),
    # Midwest Region
    ("Michigan", "UMBC/Howard"): (0.995, 0.005),
    ("Georgia", "Saint Louis"): (0.561, 0.439),
    ("Texas Tech", "Akron"): (0.761, 0.239),
    ("Alabama", "Hofstra"): (0.873, 0.127),
    ("Tennessee", "Miami OH/SMU"): (0.70, 0.30),  # Estimated
    ("Virginia", "Wright State"): (0.960, 0.040),
    ("Kentucky", "Santa Clara"): (0.570, 0.430),
    ("Iowa State", "Tennessee State"): (0.978, 0.022),
}


# =============================================================================
# HISTORICAL SEED WIN RATES (1985-2025, Bayesian priors)
# =============================================================================

HISTORICAL_SEED_WIN_RATES = {
    (1, 16): 0.988,
    (2, 15): 0.931,
    (3, 14): 0.856,
    (4, 13): 0.794,
    (5, 12): 0.644,
    (6, 11): 0.613,
    (7, 10): 0.613,
    (8, 9): 0.481,  # 9 seeds actually favored historically
}

# Historical advancement rates by seed (for later rounds)
SEED_ADVANCEMENT_RATES = {
    # seed: {round: probability of reaching that round}
    1:  {"R32": 0.988, "S16": 0.850, "E8": 0.669, "FF": 0.413, "CG": 0.263, "CHAMP": 0.163},
    2:  {"R32": 0.931, "S16": 0.644, "E8": 0.450, "FF": 0.200, "CG": 0.106, "CHAMP": 0.063},
    3:  {"R32": 0.856, "S16": 0.525, "E8": 0.256, "FF": 0.106, "CG": 0.063, "CHAMP": 0.044},
    4:  {"R32": 0.794, "S16": 0.481, "E8": 0.156, "FF": 0.094, "CG": 0.038, "CHAMP": 0.025},
    5:  {"R32": 0.644, "S16": 0.344, "E8": 0.075, "FF": 0.056, "CG": 0.019, "CHAMP": 0.000},
    6:  {"R32": 0.613, "S16": 0.294, "E8": 0.106, "FF": 0.019, "CG": 0.013, "CHAMP": 0.006},
    7:  {"R32": 0.613, "S16": 0.181, "E8": 0.063, "FF": 0.019, "CG": 0.006, "CHAMP": 0.006},
    8:  {"R32": 0.481, "S16": 0.100, "E8": 0.056, "FF": 0.038, "CG": 0.019, "CHAMP": 0.006},
    9:  {"R32": 0.519, "S16": 0.050, "E8": 0.031, "FF": 0.013, "CG": 0.000, "CHAMP": 0.000},
    10: {"R32": 0.388, "S16": 0.150, "E8": 0.056, "FF": 0.006, "CG": 0.000, "CHAMP": 0.000},
    11: {"R32": 0.388, "S16": 0.169, "E8": 0.063, "FF": 0.038, "CG": 0.000, "CHAMP": 0.000},
    12: {"R32": 0.356, "S16": 0.138, "E8": 0.013, "FF": 0.000, "CG": 0.000, "CHAMP": 0.000},
    13: {"R32": 0.206, "S16": 0.038, "E8": 0.000, "FF": 0.000, "CG": 0.000, "CHAMP": 0.000},
    14: {"R32": 0.144, "S16": 0.013, "E8": 0.000, "FF": 0.000, "CG": 0.000, "CHAMP": 0.000},
    15: {"R32": 0.069, "S16": 0.025, "E8": 0.006, "FF": 0.000, "CG": 0.000, "CHAMP": 0.000},
    16: {"R32": 0.013, "S16": 0.000, "E8": 0.000, "FF": 0.000, "CG": 0.000, "CHAMP": 0.000},
}


# ESPN Standard Scoring
ESPN_SCORING = {
    "R64": 10,
    "R32": 20,
    "S16": 40,
    "E8": 80,
    "FF": 160,
    "CG": 320,
}
