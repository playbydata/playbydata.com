from typing import Tuple, List

import pandas as pd



def qcut_series(series, q=3):
    series = pd.qcut(series, q=q)
    bin_counts = series.value_counts(sort=False)
    return bin_counts


def qcut_2d(df, x_col, y_col, qx: int = 3, qy=None) -> List[Tuple[Tuple[pd.Interval, int], Tuple[pd.Interval, int]]]:
    """"""
    # Params
    qy =qy or qx
    bins = []

    # Iterate
    x_bin_counts = qcut_series(df[x_col], q=qx)
    for x_interval, x_count in x_bin_counts.items():
        y_bin_counts = qcut_series(
            df[(df[x_col] > x_interval.left) & (df[x_col] <= x_interval.right)][y_col], q=qy)
        for y_interval, y_count in y_bin_counts.items():
            bins.append(((x_interval, x_count), (y_interval, y_count)))
    return bins