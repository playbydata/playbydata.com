import os
from typing import Optional

import pandas as pd
import nfl_data_py as nfl

from common.utils import LOCAL_STORAGE_PATH


__all__ = ("get_nfl_pbp_data",)


CACHE_FILE = os.path.join(LOCAL_STORAGE_PATH, "nfl_pbp_data.csv")
NFL_YEARS = list(range(1999, 2025, 1))


def get_nfl_pbp_data(years: Optional[list[int]] = None, use_cache: bool =True) -> pd.DataFrame:
    """"""
    if os.path.exists(CACHE_FILE) and use_cache and not years:
        return pd.read_csv(CACHE_FILE)

    import_years = years or NFL_YEARS
    nfl_df = nfl.import_pbp_data(import_years, downcast=True)
    if use_cache and not years:
        nfl_df.to_csv(CACHE_FILE, index=False)
    return nfl_df
