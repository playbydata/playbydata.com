import numpy as np
import pandas as pd


def get_nfl_per_game_per_team_df(nfl_df) -> pd.DataFrame:
    df: pd.DataFrame = (
        # Filter
        nfl_df[nfl_df['posteam'] != '']
        # Group By
        .groupby([
            'game_id', 'home_team', 'away_team', 'season_type','week', 'posteam', 'posteam_type', 'game_date',
            'season', 'location', 'div_game',	'roof', 'surface', 'temp',	'wind',	'home_coach', 'away_coach',
            'game_stadium'
        ])
        # Extra
        .agg({
            'yards_gained': 'sum',
            'air_yards': 'sum',
            'yards_after_catch': 'sum',
            'kick_distance': 'sum',
            'posteam_score_post': 'last',
            'defteam_score_post': 'last',
            'score_differential_post': 'last',
            'first_down_rush': 'sum',
            'first_down_pass': 'sum',
            'first_down_penalty': 'sum',
            'third_down_failed': 'sum',
            'third_down_converted': 'sum',
            'fourth_down_converted': 'sum',
            'fourth_down_failed': 'sum',
            'incomplete_pass': 'sum',
            'interception': 'sum',
            'rush_attempt': 'sum',
            'pass_attempt': 'sum',
            'sack': 'sum',
            'touchdown': 'sum',
            'pass_touchdown': 'sum',
            'rush_touchdown': 'sum',
            'return_touchdown': 'sum',
            'passing_yards': 'sum',
            'receiving_yards': 'sum',
            'rushing_yards': 'sum',
        })
        .reset_index()
    )
    df['winning_team_score'] = np.maximum(df['posteam_score_post'], df['defteam_score_post'])
    df['losing_team_score'] = np.minimum(df['posteam_score_post'], df['defteam_score_post'])
    df['score_diff'] = df['winning_team_score'] - df['losing_team_score']
    return df

def get_nfl_per_game_df(nfl_df) -> pd.DataFrame:
    """"""
    nfl_per_game_per_team_df = get_nfl_per_game_per_team_df(nfl_df)
    nfl_per_game_df = (
        nfl_per_game_per_team_df
        .groupby([
            'game_id', 'home_team', 'away_team', 'season_type', 'week', 'game_date', 'season', 'location', 'div_game',
            'roof', 'surface', 'temp', 'wind', 'home_coach',
            'away_coach', 'game_stadium'
        ])
        .agg({
            'yards_gained': 'sum',
            'air_yards': 'sum',
            'yards_after_catch': 'sum',
            'kick_distance': 'sum',
            'winning_team_score': 'last',
            'losing_team_score': 'last',
            'score_differential_post': 'last',
            'first_down_rush': 'sum',
            'first_down_pass': 'sum',
            'first_down_penalty': 'sum',
            'third_down_failed': 'sum',
            'third_down_converted': 'sum',
            'fourth_down_converted': 'sum',
            'fourth_down_failed': 'sum',
            'incomplete_pass': 'sum',
            'interception': 'sum',
            'rush_attempt': 'sum',
            'pass_attempt': 'sum',
            'sack': 'sum',
            'touchdown': 'sum',
            'pass_touchdown': 'sum',
            'rush_touchdown': 'sum',
            'return_touchdown': 'sum',
            'passing_yards': 'sum',
            'receiving_yards': 'sum',
            'rushing_yards': 'sum',
        })
    )
    return nfl_per_game_df
