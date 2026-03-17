"""
Load real statistical data from Bart Torvik CSV and Sports Reference CSVs.
Merges all sources and updates team_data.TEAMS with actual numbers.
"""

import csv
import os

# Name mappings: Torvik name -> our bracket name
TORVIK_NAME_MAP = {
    "Duke": "Duke", "Michigan": "Michigan", "Arizona": "Arizona",
    "Florida": "Florida", "Houston": "Houston", "Iowa St.": "Iowa State",
    "Connecticut": "UConn", "Purdue": "Purdue", "Illinois": "Illinois",
    "Michigan St.": "Michigan State", "Gonzaga": "Gonzaga",
    "Virginia": "Virginia", "Texas Tech": "Texas Tech",
    "St. John's": "St. John's", "Vanderbilt": "Vanderbilt",
    "Nebraska": "Nebraska", "Alabama": "Alabama", "Kansas": "Kansas",
    "Arkansas": "Arkansas", "Wisconsin": "Wisconsin", "BYU": "BYU",
    "Tennessee": "Tennessee", "North Carolina": "North Carolina",
    "Louisville": "Louisville", "UCLA": "UCLA", "Kentucky": "Kentucky",
    "Saint Mary's": "Saint Mary's", "Miami FL": "Miami FL",
    "Ohio St.": "Ohio State", "TCU": "TCU", "Clemson": "Clemson",
    "Iowa": "Iowa", "Villanova": "Villanova", "Utah St.": "Utah State",
    "Georgia": "Georgia", "Saint Louis": "Saint Louis",
    "North Dakota St.": "North Dakota State",
    "UCF": "UCF", "Missouri": "Missouri", "Santa Clara": "Santa Clara",
    "Texas A&M": "Texas A&M", "Akron": "Akron", "McNeese": "McNeese",
    "VCU": "VCU", "South Florida": "South Florida",
    "Cal Baptist": "Cal Baptist", "Hofstra": "Hofstra",
    "Troy": "Troy", "Kennesaw St.": "Kennesaw State",
    "Northern Iowa": "Northern Iowa", "High Point": "High Point",
    "Penn": "Penn", "Wright St.": "Wright State",
    "Furman": "Furman", "Queens": "Queens",
    "Idaho": "Idaho", "Tennessee St.": "Tennessee State",
    "Siena": "Siena", "LIU": "Long Island",
    "Hawaii": "Hawaii",
    "McNeese St.": "McNeese",
    "Miami OH": "Miami OH/SMU",  # First Four placeholder
    "SMU": "Miami OH/SMU",  # alternate
    "UMBC": "UMBC/Howard",
    "Howard": "UMBC/Howard",
    "Prairie View A&M": "Prairie View/Lehigh",
    "NC State": "Texas/NC State",
    "Texas": "Texas/NC State",
}

# Sports Reference name -> our bracket name
SR_NAME_MAP = {
    "Duke": "Duke", "Michigan": "Michigan", "Arizona": "Arizona",
    "Florida": "Florida", "Houston": "Houston",
    "Iowa State": "Iowa State", "Connecticut": "UConn",
    "Purdue": "Purdue", "Illinois": "Illinois",
    "Michigan State": "Michigan State", "Gonzaga": "Gonzaga",
    "Virginia": "Virginia", "Texas Tech": "Texas Tech",
    "St. John's (NY)": "St. John's", "Vanderbilt": "Vanderbilt",
    "Nebraska": "Nebraska", "Alabama": "Alabama", "Kansas": "Kansas",
    "Arkansas": "Arkansas", "Wisconsin": "Wisconsin",
    "Brigham Young": "BYU", "Tennessee": "Tennessee",
    "North Carolina": "North Carolina", "Louisville": "Louisville",
    "UCLA": "UCLA", "Kentucky": "Kentucky",
    "Saint Mary's (CA)": "Saint Mary's", "Miami (FL)": "Miami FL",
    "Ohio State": "Ohio State", "TCU": "TCU", "Clemson": "Clemson",
    "Iowa": "Iowa", "Villanova": "Villanova",
    "Utah State": "Utah State", "Georgia": "Georgia",
    "Saint Louis": "Saint Louis",
    "North Dakota State": "North Dakota State",
    "UCF": "UCF", "Missouri": "Missouri",
    "Santa Clara": "Santa Clara", "Texas A&M": "Texas A&M",
    "Akron": "Akron", "McNeese State": "McNeese",
    "VCU": "VCU", "South Florida": "South Florida",
    "California Baptist": "Cal Baptist", "Hofstra": "Hofstra",
    "Troy": "Troy", "Kennesaw State": "Kennesaw State",
    "Northern Iowa": "Northern Iowa", "High Point": "High Point",
    "Pennsylvania": "Penn", "Wright State": "Wright State",
    "Furman": "Furman", "Queens (NC)": "Queens",
    "Idaho": "Idaho", "Tennessee State": "Tennessee State",
    "Siena": "Siena", "LIU": "Long Island",
    "Hawaii": "Hawaii",
    "McNeese": "McNeese", "McNeese State": "McNeese",
    "Virginia Commonwealth": "VCU",
    "Long Island University": "Long Island",
    "Texas Christian": "TCU",
    "Miami (OH)": "Miami OH/SMU",
    "SMU": "Miami OH/SMU",
    "UMBC": "UMBC/Howard",
    "Howard": "UMBC/Howard",
    "Prairie View A&M": "Prairie View/Lehigh",
    "NC State": "Texas/NC State",
    "Texas": "Texas/NC State",
}

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def safe_float(val, default=0.0):
    """Convert string to float, handling empty strings and special chars."""
    if not val or val.strip() in ('', '-', '—'):
        return default
    try:
        return float(val.strip())
    except ValueError:
        return default


def load_torvik_data():
    """Load Bart Torvik CSV. Returns dict: bracket_name -> {stats}."""
    filepath = os.path.join(DATA_DIR, "barttorvik_2026.csv")
    data = {}

    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            torvik_name = row["team"]
            bracket_name = TORVIK_NAME_MAP.get(torvik_name)
            if not bracket_name:
                # Try exact match
                if torvik_name in TORVIK_NAME_MAP.values():
                    bracket_name = torvik_name
                else:
                    continue

            data[bracket_name] = {
                "torvik_rank": int(row["rank"]),
                "adjoe": safe_float(row["adjoe"]),
                "adjde": safe_float(row["adjde"]),
                "adjt": safe_float(row["adjt"]),
                "barthag": safe_float(row["barthag"]),
                "sos": safe_float(row["sos"]),
                "record": row["record"],
                "conf": row["conf"],
                "wab": safe_float(row.get("WAB", "0")),
            }

    return data


def load_sr_advanced():
    """Load Sports Reference advanced team stats."""
    filepath = os.path.join(DATA_DIR, "sports_reference_advanced_2026.csv")
    data = {}

    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sr_name = row["School"]
            bracket_name = SR_NAME_MAP.get(sr_name)
            if not bracket_name:
                if sr_name in SR_NAME_MAP.values():
                    bracket_name = sr_name
                else:
                    continue

            data[bracket_name] = {
                "efg_pct": safe_float(row.get("eFG%")),
                "tov_pct": safe_float(row.get("TOV%")),
                "orb_pct": safe_float(row.get("ORB%")),
                "ftr": safe_float(row.get("FTr")),
                "pace": safe_float(row.get("Pace")),
                "ortg_raw": safe_float(row.get("ORtg")),
                "srs": safe_float(row.get("SRS")),
                "ts_pct": safe_float(row.get("TS%")),
            }

    return data


def load_sr_basic():
    """Load Sports Reference basic team stats (for 3P%, FT%, FG%)."""
    filepath = os.path.join(DATA_DIR, "sports_reference_basic_2026.csv")
    data = {}

    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sr_name = row["School"]
            bracket_name = SR_NAME_MAP.get(sr_name)
            if not bracket_name:
                if sr_name in SR_NAME_MAP.values():
                    bracket_name = sr_name
                else:
                    continue

            data[bracket_name] = {
                "fg_pct": safe_float(row.get("FG%")),
                "three_pt_pct": safe_float(row.get("3P%")),
                "ft_pct": safe_float(row.get("FT%")),
            }

    return data


def load_sr_opponent_basic():
    """Load Sports Reference opponent basic stats (for Opp 3P%, FG%)."""
    filepath = os.path.join(DATA_DIR, "sports_reference_opponent_stats_2026.csv")
    data = {}

    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sr_name = row["School"]
            bracket_name = SR_NAME_MAP.get(sr_name)
            if not bracket_name:
                if sr_name in SR_NAME_MAP.values():
                    bracket_name = sr_name
                else:
                    continue

            data[bracket_name] = {
                "opp_fg_pct": safe_float(row.get("FG%")),
                "opp_three_pt_pct": safe_float(row.get("3P%")),
                "opp_ft_pct": safe_float(row.get("FT%")),
            }

    return data


def load_sr_opponent_advanced():
    """Load Sports Reference opponent advanced stats."""
    filepath = os.path.join(DATA_DIR, "sports_reference_opponent_advanced_2026.csv")
    data = {}

    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sr_name = row["School"]
            bracket_name = SR_NAME_MAP.get(sr_name)
            if not bracket_name:
                if sr_name in SR_NAME_MAP.values():
                    bracket_name = sr_name
                else:
                    continue

            data[bracket_name] = {
                "opp_efg_pct": safe_float(row.get("eFG%")),
                "opp_tov_pct": safe_float(row.get("TOV%")),
                "opp_orb_pct": safe_float(row.get("ORB%")),
                "opp_ftr": safe_float(row.get("FTr")),
            }

    return data


def load_espn_bpi():
    """Load ESPN Basketball Power Index data for all 365 teams.
    Third independent power rating system for our ensemble."""
    filepath = os.path.join(DATA_DIR, "espn_bpi_all_teams.csv")
    data = {}

    if not os.path.exists(filepath):
        return data

    # ESPN name -> bracket name mapping
    ESPN_MAP = {
        "Duke Blue Devils": "Duke", "Michigan Wolverines": "Michigan",
        "Arizona Wildcats": "Arizona", "Florida Gators": "Florida",
        "Houston Cougars": "Houston", "Iowa State Cyclones": "Iowa State",
        "Connecticut Huskies": "UConn", "Purdue Boilermakers": "Purdue",
        "Illinois Fighting Illini": "Illinois",
        "Michigan State Spartans": "Michigan State",
        "Gonzaga Bulldogs": "Gonzaga", "Virginia Cavaliers": "Virginia",
        "Texas Tech Red Raiders": "Texas Tech",
        "St. John's Red Storm": "St. John's",
        "Vanderbilt Commodores": "Vanderbilt",
        "Nebraska Cornhuskers": "Nebraska", "Alabama Crimson Tide": "Alabama",
        "Kansas Jayhawks": "Kansas", "Arkansas Razorbacks": "Arkansas",
        "Wisconsin Badgers": "Wisconsin", "BYU Cougars": "BYU",
        "Tennessee Volunteers": "Tennessee",
        "North Carolina Tar Heels": "North Carolina",
        "Louisville Cardinals": "Louisville", "UCLA Bruins": "UCLA",
        "Kentucky Wildcats": "Kentucky",
        "Saint Mary's Gaels": "Saint Mary's",
        "Miami Hurricanes": "Miami FL",
        "Ohio State Buckeyes": "Ohio State", "TCU Horned Frogs": "TCU",
        "Clemson Tigers": "Clemson", "Iowa Hawkeyes": "Iowa",
        "Villanova Wildcats": "Villanova",
        "Utah State Aggies": "Utah State",
        "Georgia Bulldogs": "Georgia", "Saint Louis Billikens": "Saint Louis",
        "North Dakota State Bison": "North Dakota State",
        "UCF Knights": "UCF", "Missouri Tigers": "Missouri",
        "Santa Clara Broncos": "Santa Clara",
        "Texas A&M Aggies": "Texas A&M",
        "Akron Zips": "Akron", "McNeese Cowboys": "McNeese",
        "VCU Rams": "VCU", "South Florida Bulls": "South Florida",
        "California Baptist Lancers": "Cal Baptist",
        "Hofstra Pride": "Hofstra", "Troy Trojans": "Troy",
        "Kennesaw State Owls": "Kennesaw State",
        "Northern Iowa Panthers": "Northern Iowa",
        "High Point Panthers": "High Point",
        "Penn Quakers": "Penn", "Wright State Raiders": "Wright State",
        "Furman Paladins": "Furman", "Queens Royals": "Queens",
        "Idaho Vandals": "Idaho",
        "Tennessee State Tigers": "Tennessee State",
        "Siena Saints": "Siena", "LIU Sharks": "Long Island",
        "Hawai'i Rainbow Warriors": "Hawaii",
    }

    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            espn_name = row.get("Team", "")
            bracket_name = ESPN_MAP.get(espn_name)
            if not bracket_name:
                continue

            bpi = safe_float(row.get("BPI"))
            off_bpi = safe_float(row.get("Off_BPI"))
            def_bpi = safe_float(row.get("Def_BPI"))
            title_pct = safe_float(row.get("Win_Title_Pct"))
            ff_pct = safe_float(row.get("Final_Four_Pct"))
            bpi_rank = safe_float(row.get("BPI_Rank"))

            data[bracket_name] = {
                "espn_bpi": bpi,
                "espn_off_bpi": off_bpi,
                "espn_def_bpi": def_bpi,
                "espn_bpi_rank": int(bpi_rank) if bpi_rank else 999,
                "espn_title_pct": title_pct,
                "espn_ff_pct": ff_pct,
            }

    return data


def load_sonny_moore():
    """Load Sonny Moore Power Ratings — point-spread based system.
    Fourth independent rating for our ensemble."""
    filepath = os.path.join(DATA_DIR, "sonny_moore_power_ratings_2026.csv")
    data = {}

    if not os.path.exists(filepath):
        return data

    # Sonny Moore uses different team names
    SM_MAP = {
        "Duke": "Duke", "Michigan": "Michigan", "Arizona": "Arizona",
        "Florida": "Florida", "Houston": "Houston",
        "Iowa St.": "Iowa State", "Connecticut": "UConn",
        "Purdue": "Purdue", "Illinois": "Illinois",
        "Michigan St.": "Michigan State", "Gonzaga": "Gonzaga",
        "Virginia": "Virginia", "Texas Tech": "Texas Tech",
        "St. John's": "St. John's", "Vanderbilt": "Vanderbilt",
        "Nebraska": "Nebraska", "Alabama": "Alabama", "Kansas": "Kansas",
        "Arkansas": "Arkansas", "Wisconsin": "Wisconsin", "BYU": "BYU",
        "Tennessee": "Tennessee", "North Carolina": "North Carolina",
        "Louisville": "Louisville", "UCLA": "UCLA", "Kentucky": "Kentucky",
        "Saint Mary's": "Saint Mary's", "Miami FL": "Miami FL",
        "Ohio St.": "Ohio State", "TCU": "TCU", "Clemson": "Clemson",
        "Iowa": "Iowa", "Villanova": "Villanova",
        "Utah St.": "Utah State", "Georgia": "Georgia",
        "Saint Louis": "Saint Louis", "UCF": "UCF",
        "Missouri": "Missouri", "Santa Clara": "Santa Clara",
        "Texas A&M": "Texas A&M", "Akron": "Akron",
        "McNeese St.": "McNeese", "VCU": "VCU",
        "South Florida": "South Florida",
        "Cal Baptist": "Cal Baptist", "Hofstra": "Hofstra",
        "Troy": "Troy", "Kennesaw St.": "Kennesaw State",
        "Northern Iowa": "Northern Iowa", "High Point": "High Point",
        "Penn": "Penn", "Wright St.": "Wright State",
        "Furman": "Furman", "Queens": "Queens",
        "Idaho": "Idaho", "Tennessee St.": "Tennessee State",
        "Siena": "Siena", "LIU": "Long Island", "Hawaii": "Hawaii",
        "North Dakota St.": "North Dakota State",
    }

    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sm_name = row.get("team", "")
            bracket_name = SM_MAP.get(sm_name)
            if not bracket_name:
                if sm_name in SM_MAP.values():
                    bracket_name = sm_name
                else:
                    continue

            data[bracket_name] = {
                "sm_rank": int(row.get("rank", 999)),
                "sm_power": safe_float(row.get("power_rating")),
                "sm_sos": safe_float(row.get("sos")),
            }

    return data


def load_sr_adjusted_ratings():
    """Load Sports Reference adjusted offensive/defensive ratings.
    These are INDEPENDENT from Torvik — gives us a second power rating system."""
    filepath = os.path.join(DATA_DIR, "sr_adjusted_ratings_2026.csv")
    data = {}

    if not os.path.exists(filepath):
        return data

    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sr_name = row["School"]
            bracket_name = SR_NAME_MAP.get(sr_name)
            if not bracket_name:
                if sr_name in SR_NAME_MAP.values():
                    bracket_name = sr_name
                else:
                    continue

            data[bracket_name] = {
                "sr_adj_ortg": safe_float(row.get("SR_AdjORtg")),
                "sr_adj_drtg": safe_float(row.get("SR_AdjDRtg")),
                "sr_adj_nrtg": safe_float(row.get("SR_AdjNRtg")),
            }

    return data


def load_all_real_data():
    """
    Load and merge all data sources.
    Returns dict: bracket_name -> {all merged stats}
    """
    torvik = load_torvik_data()
    sr_adv = load_sr_advanced()
    sr_basic = load_sr_basic()
    sr_opp_basic = load_sr_opponent_basic()
    sr_opp_adv = load_sr_opponent_advanced()
    sr_ratings = load_sr_adjusted_ratings()
    espn_bpi = load_espn_bpi()
    sonny_moore = load_sonny_moore()

    merged = {}

    # Start with Torvik (has the best quality-adjusted ratings)
    for team, stats in torvik.items():
        merged[team] = dict(stats)

    # Merge Sports Reference data
    for team in merged:
        if team in sr_adv:
            merged[team].update(sr_adv[team])
        if team in sr_basic:
            merged[team].update(sr_basic[team])
        if team in sr_opp_basic:
            merged[team].update(sr_opp_basic[team])
        if team in sr_opp_adv:
            merged[team].update(sr_opp_adv[team])
        if team in sr_ratings:
            merged[team].update(sr_ratings[team])
        if team in espn_bpi:
            merged[team].update(espn_bpi[team])
        if team in sonny_moore:
            merged[team].update(sonny_moore[team])

    # Also add BPI teams that might not be in Torvik
    for team, stats in espn_bpi.items():
        if team not in merged:
            merged[team] = dict(stats)

    return merged


def update_teams_with_real_data(teams_dict):
    """
    Update the TEAMS dictionary in team_data.py with real data.
    Preserves manually-set fields like injury_factor, momentum, coach_tourney_exp.
    """
    real_data = load_all_real_data()

    updated = 0
    missing = []

    for team_name, team_info in teams_dict.items():
        # Skip First Four placeholders
        if "/" in team_name:
            continue

        if team_name not in real_data:
            missing.append(team_name)
            continue

        rd = real_data[team_name]

        # Update with real Torvik data
        if "adjoe" in rd:
            team_info["kenpom_em"] = rd["adjoe"] - rd["adjde"]
            team_info["_real_adjoe"] = rd["adjoe"]
            team_info["_real_adjde"] = rd["adjde"]
            team_info["_real_adjt"] = rd["adjt"]
            team_info["_real_barthag"] = rd["barthag"]
            team_info["_real_torvik_rank"] = rd["torvik_rank"]

        if "record" in rd:
            team_info["record"] = rd["record"]
            parts = rd["record"].split("-")
            if len(parts) == 2:
                w, l = int(parts[0]), int(parts[1])
                team_info["record_pct"] = w / (w + l) if (w + l) > 0 else 0.5

        # Update Four Factors from Sports Reference
        if "efg_pct" in rd and rd["efg_pct"] > 0:
            team_info["_real_efg_pct"] = rd["efg_pct"]
        if "tov_pct" in rd and rd["tov_pct"] > 0:
            team_info["to_rate"] = rd["tov_pct"] / 100  # Convert from percentage
            team_info["_real_tov_pct"] = rd["tov_pct"]
        if "orb_pct" in rd and rd["orb_pct"] > 0:
            team_info["oreb_pct"] = rd["orb_pct"] / 100  # Convert from percentage
            team_info["_real_orb_pct"] = rd["orb_pct"]
        if "ftr" in rd and rd["ftr"] > 0:
            team_info["_real_ftr"] = rd["ftr"]

        # Update shooting stats
        if "three_pt_pct" in rd and rd["three_pt_pct"] > 0:
            team_info["fg_pct_3pt"] = rd["three_pt_pct"]
        if "ft_pct" in rd and rd["ft_pct"] > 0:
            team_info["ft_pct"] = rd["ft_pct"]

        # Update opponent stats
        if "opp_three_pt_pct" in rd and rd["opp_three_pt_pct"] > 0:
            team_info["opp_fg_pct_3pt"] = rd["opp_three_pt_pct"]
        if "opp_efg_pct" in rd:
            team_info["_real_opp_efg_pct"] = rd["opp_efg_pct"]

        # Update pace
        if "pace" in rd and rd["pace"] > 0:
            team_info["_real_pace"] = rd["pace"]

        # SRS / SOS
        if "srs" in rd:
            team_info["_real_srs"] = rd["srs"]
        if "sos" in rd:
            team_info["_real_sos"] = rd["sos"]

        # SR Adjusted Ratings (independent second power rating system)
        if "sr_adj_ortg" in rd and rd["sr_adj_ortg"] > 0:
            team_info["_sr_adj_ortg"] = rd["sr_adj_ortg"]
            team_info["_sr_adj_drtg"] = rd["sr_adj_drtg"]
            team_info["_sr_adj_nrtg"] = rd["sr_adj_nrtg"]

        # ESPN BPI (independent third power rating system)
        if "espn_bpi" in rd and rd["espn_bpi"] != 0:
            team_info["_espn_bpi"] = rd["espn_bpi"]
            team_info["_espn_off_bpi"] = rd["espn_off_bpi"]
            team_info["_espn_def_bpi"] = rd["espn_def_bpi"]
            team_info["_espn_bpi_rank"] = rd["espn_bpi_rank"]
            team_info["_espn_title_pct"] = rd["espn_title_pct"]

        # Sonny Moore Power Ratings (independent fourth system)
        if "sm_power" in rd and rd["sm_power"] > 0:
            team_info["_sm_power"] = rd["sm_power"]
            team_info["_sm_rank"] = rd["sm_rank"]

        updated += 1

    return updated, missing


if __name__ == "__main__":
    # Test the data loading
    real = load_all_real_data()

    print(f"Loaded real data for {len(real)} teams")
    print()

    # Show tournament teams
    from team_data import TEAMS
    print(f"{'Team':<22} {'Torvik':>6} {'AdjOE':>7} {'AdjDE':>7} {'AdjEM':>7} {'AdjT':>6} {'eFG%':>6} {'TOV%':>6} {'ORB%':>6} {'3P%':>6} {'Opp3P%':>7} {'FT%':>6}")
    print("-" * 110)

    for team_name in TEAMS:
        if "/" in team_name:
            continue
        if team_name not in real:
            print(f"{team_name:<22} MISSING")
            continue

        rd = real[team_name]
        em = rd.get("adjoe", 0) - rd.get("adjde", 0)
        print(f"{team_name:<22} "
              f"{rd.get('torvik_rank', '?'):>6} "
              f"{rd.get('adjoe', 0):>7.1f} "
              f"{rd.get('adjde', 0):>7.1f} "
              f"{em:>+7.1f} "
              f"{rd.get('adjt', 0):>6.1f} "
              f"{rd.get('efg_pct', 0):>6.3f} "
              f"{rd.get('tov_pct', 0):>6.1f} "
              f"{rd.get('orb_pct', 0):>6.1f} "
              f"{rd.get('three_pt_pct', 0):>6.3f} "
              f"{rd.get('opp_three_pt_pct', 0):>7.3f} "
              f"{rd.get('ft_pct', 0):>6.3f}")
