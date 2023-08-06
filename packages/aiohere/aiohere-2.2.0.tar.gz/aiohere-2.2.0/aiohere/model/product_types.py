"""Available Product Types."""

from enum import Enum


class WeatherProductType(Enum):
    """Identifies the type of report to obtain."""

    OBSERVATION = "observation"
    FORECAST_7DAYS = "forecast7days"
    FORECAST_7DAYS_SIMPLE = "forecast7dayssimple"
    FORECAST_HOURLY = "forecastHourly"
    FORECAST_ASTRONOMY = "forecastAstronomy"
    ALERTS = "alerts"
    NWS_ALERTS = "nws_alerts"

    def __str__(self):
        return f"{self.value}"
