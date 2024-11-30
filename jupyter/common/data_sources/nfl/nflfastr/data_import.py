import os
from typing import Optional

import pandas as pd
import nfl_data_py as nfl

from common.cache import cache_backend
import settings


__all__ = ("get_nfl_pbp_data",)


NFL_PBP_DATA_CACHE_PREFIX = "nfl_pbp_data_df"
NFL_YEARS = list(range(1999, 2025, 1))


def get_nfl_pbp_data(years: Optional[list[int]] = None, use_cache: bool = True) -> pd.DataFrame:
    """"""
    from common.data_sources.nfl.nflfastr.transform import add_extra_nfl_pbp_df
    if not years:
        cache_path = NFL_PBP_DATA_CACHE_PREFIX
    elif len(years) == 1:
        cache_path = f"{NFL_PBP_DATA_CACHE_PREFIX}_{years[0]}"
    else:
        cache_path = f"{NFL_PBP_DATA_CACHE_PREFIX}_{years[0]}_{years[1]}"

    if not settings.RESET_CACHE:
        nfl_df = cache_backend.get(cache_path)
        print(f"Cached {isinstance(nfl_df, pd.DataFrame)}")
        if isinstance(nfl_df, pd.DataFrame):
            print(cache_path)
            return nfl_df
    import_years = years or NFL_YEARS
    nfl_df = nfl.import_pbp_data(import_years, downcast=False)
    nfl_df = add_extra_nfl_pbp_df(nfl_df)
    cache_backend.set(cache_path, nfl_df)
    return nfl_df
