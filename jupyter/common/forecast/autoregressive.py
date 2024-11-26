import dataclasses
from typing import Optional

import numpy as np
from statsmodels.tsa.ar_model import AutoReg

from .base import BaseForecat


@dataclasses.dataclass
class AutoRegressiveForecast(BaseForecat):
    """"""
    lags: Optional[int] = None

    def forecast(self):
        model = AutoReg(self.train_data, lags=self.lags)
        model = model.fit()
        forecast = model.forecast().values[0]
        return forecast
