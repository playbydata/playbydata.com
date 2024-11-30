import dataclasses
from typing import Optional

import pandas as pd
from sklearn.metrics import mean_squared_error

from .base import BaseForecat


@dataclasses.dataclass
class MovingAverageForecast(BaseForecat):
    """"""
    interval: Optional[int] = None
    interval_range: Optional[list[int]] = None

    def forecast(self):
        moving_averages = self.train_data.rolling(self.interval).mean()
        return moving_averages.iloc[-1]

    def forecast_series(self, test_data):
        if self.interval_range and not self.interval:
            self.interval = self.optimize_interval(test_data, self.interval_range)
        return super().forecast_series(test_data)

    def optimize_interval(self, test_data, interval_range):
        """
        Run Forecast through the interval_range and minimize the `mse`
        """
        mse_df = pd.DataFrame({"interval": interval_range, "mse": [None for i in interval_range]})
        for i in range(len(mse_df)):
            ar_forecaster = MovingAverageForecast(train_data=self.train_data, interval=mse_df.loc[i, "interval"])
            forecast_data = ar_forecaster.forecast_series(test_data)
            mse = mean_squared_error(test_data, forecast_data)
            mse_df.loc[i, "mse"] = mse
        return mse_df[mse_df["mse"] == mse_df["mse"].min()].iloc[0]["interval"]
