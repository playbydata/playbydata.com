import numpy as np
import pandas as pd


GROUPBY_FIELDS = [
    "game_id",
    "home_team",
    "away_team",
    "season_type",
    "week",
    "game_date",
    "season",
    "location",
    "div_game",
    # "roof",
    # "surface",
    # "temp",
    # "wind",
    "home_coach",
    "away_coach",
    "game_stadium"
]

AGGREGATION_FIELDS  = {
    "yards_gained": "sum",
    "air_yards": "sum",
    "yards_after_catch": "sum",
    "kick_distance": "sum",
    "first_down_rush": "sum",
    "first_down_pass": "sum",
    "first_down_penalty": "sum",
    "third_down_failed": "sum",
    "third_down_converted": "sum",
    "fourth_down_converted": "sum",
    "fourth_down_failed": "sum",
    "incomplete_pass": "sum",
    "interception": "sum",
    "rush_attempt": "sum",
    "pass_attempt": "sum",
    "sack": "sum",
    "touchdown": "sum",
    "pass_touchdown": "sum",
    "rush_touchdown": "sum",
    "return_touchdown": "sum",
    "passing_yards": "sum",
    "receiving_yards": "sum",
    "rushing_yards": "sum",
    "extra_point_count": "sum",
    "two_point_conv_count": "sum",
    "field_goal_count": "sum",
    "posteam_score_play_diff": "sum",
    "defteam_score_play_diff": "sum",
    "safety": "sum"
}


def add_extra_nfl_pbp_df(nfl_df) -> pd.DataFrame:
    nfl_df["extra_point_count"] = nfl_df["extra_point_result"].apply(lambda x: 1 if x == "good" else 0)
    nfl_df["two_point_conv_count"] = nfl_df["two_point_conv_result"].apply(lambda x: 1 if x == "success" else 0)
    nfl_df["field_goal_count"] = nfl_df["field_goal_result"].apply(lambda x: 1 if x == "made" else 0)
    nfl_df["posteam_score_play_diff"] = nfl_df["posteam_score_post"] - nfl_df["posteam_score"]
    nfl_df["defteam_score_play_diff"] = nfl_df["defteam_score_post"] - nfl_df["defteam_score"]
    nfl_df = nfl_df[nfl_df["time"].str.match(r"^\d+:\d+$", na=False)].copy()
    nfl_df[["total_minutes", "total_minutes_rounded"]] = nfl_df.apply(
        lambda row: pd.Series({
            "total_minutes": (row["qtr"] - 1) * 15 + (15 - int(row["time"].split(":")[0])) + int(
                row["time"].split(":")[1]) / 60,
            "total_minutes_rounded": round(
                (row["qtr"] - 1) * 15 + (15 - int(row["time"].split(":")[0])) + int(row["time"].split(":")[1]) / 60)
        }),
        axis=1
    )
    return nfl_df

def get_nfl_offensive_per_game_per_team_df(nfl_df) -> pd.DataFrame:
    # nfl_df = add_extra_nfl_pbp_df(nfl_df)
    df: pd.DataFrame = (
        # Filter
        nfl_df[nfl_df["posteam"] != ""]
        # Group By
        .groupby(GROUPBY_FIELDS + [ "posteam", "posteam_type"])
        # Extra
        .agg({
            **AGGREGATION_FIELDS,
            "posteam_score_post": "last",
            "defteam_score_post": "last",
            "score_differential_post": "last",
            "posteam_score_play_diff": "sum",
        })
        .reset_index()
    )
    df = df.dropna()
    df["winning_team_score"] = np.maximum(df["posteam_score_post"], df["defteam_score_post"])
    df["losing_team_score"] = np.minimum(df["posteam_score_post"], df["defteam_score_post"])
    df["score_diff"] = df["winning_team_score"] - df["losing_team_score"]
    df["score_total"] = df["winning_team_score"] + df["losing_team_score"]
    df["team_def_points"] = df["posteam_score_post"] - df["posteam_score_play_diff"]
    return df

def get_nfl_per_game_df(nfl_df) -> pd.DataFrame:
    """"""
    # nfl_df = add_extra_nfl_pbp_df(nfl_df)
    df = (
        nfl_df
        .groupby(GROUPBY_FIELDS)
        .agg({
            **AGGREGATION_FIELDS,
            "posteam_score_post": "last",
            "defteam_score_post": "last",
            "posteam_score_play_diff": "sum",
            "defteam_score_play_diff": "sum",
        })
    )
    df = df.dropna()
    df["winning_team_score"] = np.maximum(df["posteam_score_post"], df["defteam_score_post"])
    df["losing_team_score"] = np.minimum(df["posteam_score_post"], df["defteam_score_post"])
    df["score_diff"] = df["winning_team_score"] - df["losing_team_score"]
    df["score_total"] = df["winning_team_score"] + df["losing_team_score"]
    return df
