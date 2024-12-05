

def first_above_threshold(series, threshold=0.05, upper_limit=0.95):
    filtered_series = series[(series > threshold) & (series < upper_limit)]
    return filtered_series.iloc[0] if not filtered_series.empty else None