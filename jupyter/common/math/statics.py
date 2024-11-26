import pandas as pd


__all__ = ('kurtosis', 'skewness', 'autocorr')


def kurtosis(x):
    return ((x - x.mean())**4 / x.var()**2).sum()

def skewness(x):
    return ((x - x.mean())**3 / x.std()**3).sum()


def autocorr(data: pd.Series, n=1):
    corr_df = pd.DataFrame({'t': data})
    for i in range(1, n+1):
        data = data.shift(1)
        corr_df[f't-{i}'] = data
    return corr_df.corr()
