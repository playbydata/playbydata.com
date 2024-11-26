import abc
import dataclasses
import numpy as np

from typing import Any, Optional


@dataclasses.dataclass
class BaseForecat(abc.ABC):
    """"""
    train_data: Optional[Any] = None
    validation_data: Optional[Any] = None

    @abc.abstractmethod
    def forecast(self):
        pass

    def forecast_series(self, test_data):
        """"""
        # Create Empty Forecast
        forecast_data = np.empty((len(test_data),))

        # Iterate
        for i in range(len(test_data)):
            forecast = self.forecast()
            forecast_data[i] = forecast
            # Attach Real Value for next forecasting
            self.train_data.loc[len(self.train_data)] = test_data.loc[i]
        return forecast_data
