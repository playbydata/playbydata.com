import numpy as np
import pandas as pd

from common.cache import cache_backend


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
    "game_stadium",
    "home_score",
    "away_score",
    "winning_team_type",
    "score_diff_total",
    "winning_team_score_total",
    "losing_team_score_total",
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
    "posteam_score_diff": "sum",
    "defteam_score_diff": "sum",
    "safety": "sum",
    "vegas_home_wp": "first",
}


def add_extra_nfl_pbp_df(nfl_df) -> pd.DataFrame:
    nfl_df["extra_point_count"] = nfl_df["extra_point_result"].apply(lambda x: 1 if x == "good" else 0)
    nfl_df["two_point_conv_count"] = nfl_df["two_point_conv_result"].apply(lambda x: 1 if x == "success" else 0)
    nfl_df["field_goal_count"] = nfl_df["field_goal_result"].apply(lambda x: 1 if x == "made" else 0)
    nfl_df["posteam_score_diff"] = nfl_df["posteam_score_post"] - nfl_df["posteam_score"]
    nfl_df["defteam_score_diff"] = nfl_df["defteam_score_post"] - nfl_df["defteam_score"]
    nfl_df = nfl_df[nfl_df["time"].str.match(r"^\d+:\d+$", na=False)].copy()
    nfl_df["winning_team_type"] = nfl_df.apply(lambda x: "home" if x["home_score"] > x["away_score"] else "away", axis=1)
    nfl_df["vegas_away_wp"] = 1 - nfl_df["vegas_home_wp"]
    nfl_df[["total_minutes", "winning_team_score", "losing_team_score"]] = nfl_df.apply(
        lambda row: pd.Series({
            "total_minutes": (row["qtr"] - 1) * 15 + (15 - int(row["time"].split(":")[0])) - int(row["time"].split(":")[1]) / 60,
            "winning_team_score": row["posteam_score_post"] if row["posteam_type"] == row["winning_team_type"] else row["defteam_score_post"],
            "losing_team_score": row["posteam_score_post"] if row["posteam_type"] != row["winning_team_type"] else row["defteam_score_post"]
        }),
        axis=1
    )
    nfl_df["total_minutes_rounded"] = nfl_df["total_minutes"].apply(lambda x: round(x))
    nfl_df["winning_team_score_total"] = np.maximum(nfl_df["home_score"], nfl_df["away_score"])
    nfl_df["losing_team_score_total"] = np.minimum(nfl_df["home_score"], nfl_df["away_score"])
    nfl_df["score_diff_total"] = nfl_df["winning_team_score_total"] - nfl_df["losing_team_score_total"]
    return nfl_df


@cache_backend.memoize(expire=60 * 60, name="get_nf_per_team")
def get_nf_per_team(nfl_df) -> pd.DataFrame:
    """"""
    filtered_df = nfl_df[
        (nfl_df["posteam"] != "") & (nfl_df["defteam"] != "") & (nfl_df["posteam"].notna())& (nfl_df["posteam"].notna())
    ].copy()
    nfl_per_play_per_team_df = (
        pd.concat([
            filtered_df.assign(
                team=nfl_df['posteam'],
                play_type='offense',
                opponent_team=nfl_df['defteam'],
                team_type=nfl_df['posteam_type'],
                team_score_final=nfl_df.apply(lambda row: row["home_score"] if row["posteam_type"] == "home" else row["away_score"], axis=1),
                opponent_team_score_final=nfl_df.apply(lambda row: row["away_score"] if row["posteam_type"] == "home" else row["home_score"], axis=1),
                team_score_pre=nfl_df['posteam_score'],
                team_score_post=nfl_df['posteam_score_post'],
                opponent_team_score_pre=nfl_df['defteam_score'],
                opponent_team_score_post=nfl_df['defteam_score_post'],
                team_score_diff_pre=nfl_df['posteam_score'] - nfl_df['defteam_score'],
                team_score_diff_post=nfl_df['posteam_score_post'] - nfl_df['defteam_score_post'],
                team_vegas_wp=nfl_df.apply(lambda row: row["vegas_home_wp"] if row["posteam_type"] == "home" else row["vegas_away_wp"], axis=1),
                opponent_team_vegas_wp=nfl_df.apply(lambda row: row["vegas_away_wp"] if row["posteam_type"] == "home" else row["vegas_home_wp"], axis=1),
                team_vegas_spread=nfl_df.apply(lambda row: row["spread_line"] if row["posteam_type"] == "home" else -1*row["spread_line"], axis=1),
            ),
            filtered_df.assign(
                team=nfl_df['defteam'],
                play_type='defense',
                opponent_team=nfl_df['posteam'],
                team_type=nfl_df['posteam_type'].apply(lambda x: "away" if x == "home" else "home"),
                team_score_final=nfl_df.apply(lambda row: row["away_score"] if row["posteam_type"] == "home" else row["home_score"], axis=1),
                opponent_team_score_final=nfl_df.apply(lambda row: row["home_score"] if row["posteam_type"] == "home" else row["away_score"], axis=1),
                team_score_pre=nfl_df['defteam_score'],
                team_score_post=nfl_df['defteam_score_post'],
                opponent_team_score_pre=nfl_df['posteam_score'],
                opponent_team_score_post=nfl_df['posteam_score_post'],
                team_score_diff_pre=nfl_df['defteam_score'] - nfl_df['posteam_score'],
                team_score_diff_post=nfl_df['defteam_score_post'] - nfl_df['posteam_score_post'],
                team_vegas_wp=nfl_df.apply(lambda row: row["vegas_away_wp"] if row["posteam_type"] == "home" else row["vegas_home_wp"], axis=1),
                opponent_team_vegas_wp=nfl_df.apply(lambda row: row["vegas_home_wp"] if row["posteam_type"] == "home" else row["vegas_away_wp"], axis=1),
                team_vegas_spread=nfl_df.apply(lambda row: -1*row["spread_line"] if row["posteam_type"] == "home" else row["spread_line"], axis=1),
            )
        ]).sort_index().reset_index(drop=True)
    )
    nfl_per_play_per_team_df['team_is_winner_vegas_spread'] = nfl_per_play_per_team_df['team_vegas_spread'].apply(lambda x: 1 if x > 0 else 0)
    nfl_per_play_per_team_df["team_score_diff_final"] = nfl_per_play_per_team_df["team_score_final"] - nfl_per_play_per_team_df["opponent_team_score_final"]
    nfl_per_play_per_team_df["is_winner_pre"] = nfl_per_play_per_team_df.apply(lambda row: "1" if row["team_score_pre"] > row["opponent_team_score_pre"] else "0", axis=1)
    nfl_per_play_per_team_df["is_winner_post"] = nfl_per_play_per_team_df.apply(lambda row: "1" if row["team_score_post"] > row["opponent_team_score_post"] else "0", axis=1)
    nfl_per_play_per_team_df["is_winner_final"] = nfl_per_play_per_team_df.apply(lambda row: "1" if row["team_score_final"] > row["opponent_team_score_final"] else "0", axis=1)
    nfl_per_play_per_team_df["opponent_team_vegas_spread"] = -1*nfl_per_play_per_team_df["team_vegas_spread"]
    return nfl_per_play_per_team_df



def get_nfl_offensive_per_game_per_team_df(nfl_df) -> pd.DataFrame:
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
            "posteam_score_diff": "sum",
        })
        .reset_index()
    )
    df = df.dropna()
    df["winning_team_score"] = np.maximum(df["posteam_score_post"], df["defteam_score_post"])
    df["losing_team_score"] = np.minimum(df["posteam_score_post"], df["defteam_score_post"])
    df["score_diff"] = df["winning_team_score"] - df["losing_team_score"]
    df["score_total"] = df["winning_team_score"] + df["losing_team_score"]
    df["team_def_points"] = df["posteam_score_post"] - df["posteam_score_diff"]
    return df

def get_nfl_per_game_df(nfl_df) -> pd.DataFrame:
    """"""
    df = (
        nfl_df
        .groupby(GROUPBY_FIELDS)
        .agg({
            **AGGREGATION_FIELDS,
            "posteam_score_post": "last",
            "defteam_score_post": "last",
            "posteam_score_diff": "sum",
            "defteam_score_diff": "sum",
        })
        .reset_index()
    )
    df = df.dropna()
    df["winning_team_score"] = np.maximum(df["posteam_score_post"], df["defteam_score_post"])
    df["losing_team_score"] = np.minimum(df["posteam_score_post"], df["defteam_score_post"])
    df["score_diff"] = df["winning_team_score"] - df["losing_team_score"]
    df["score_total"] = df["winning_team_score"] + df["losing_team_score"]
    return df


def get_nfl_per_game_per_minute_df(nfl_df) -> pd.DataFrame:
    """"""
    df = (
        nfl_df
        .groupby(GROUPBY_FIELDS + [ "total_minutes_rounded"])
        .agg({
            **AGGREGATION_FIELDS,
            "winning_team_score": "last",
            "losing_team_score": "last",
            "posteam_score_post": "last",
            "defteam_score_post": "last",
        })
        .reset_index()
    )
    df = df.dropna()
    df["score_diff"] = df["winning_team_score"] - df["losing_team_score"]
    df["score_total"] = df["winning_team_score"] + df["losing_team_score"]
    return df


def get_nfl_per_game_per_qtr_df(nfl_df) -> pd.DataFrame:
    """"""
    df = (
        nfl_df
        .groupby(GROUPBY_FIELDS + [ "qtr"])
        .agg({
            **AGGREGATION_FIELDS,
            "winning_team_score": "last",
            "losing_team_score": "last",
            "posteam_score_post": "last",
            "defteam_score_post": "last",
        })
        .reset_index()
    )
    df = df.dropna()
    df["score_diff"] = df["winning_team_score"] - df["losing_team_score"]
    df["score_total"] = df["winning_team_score"] + df["losing_team_score"]
    return df