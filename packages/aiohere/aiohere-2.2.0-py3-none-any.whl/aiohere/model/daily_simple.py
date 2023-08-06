"""Daily response model."""

from typing import TypedDict

from .place import Place


class DailySimpleForecast(TypedDict):
    """DailySimple Forecast"""

    daylight: str
    description: str
    skyInfo: int
    skyDesc: str
    temperatureDesc: str
    comfort: float
    highTemperature: float
    lowTemperature: float
    humidity: int
    dewPoint: float
    precipitationProbability: int
    precipitationDesc: str
    snowFall: float
    windSpeed: float
    windDirection: int
    windDesc: str
    windDescShort: str
    beaufortScale: int
    beaufortDesc: str
    uvIndex: int
    uvDesc: str
    barometerPressure: float
    iconId: int
    iconName: str
    iconLink: str
    weekday: str
    time: str


class DailySimpleForecasts(TypedDict):
    """DailySimple Forecasts"""

    place: Place
    forecasts: list[DailySimpleForecast]


class DailySimpleResponse(TypedDict):
    """DailySimple Response"""

    dailyForecasts: list[DailySimpleForecasts]
