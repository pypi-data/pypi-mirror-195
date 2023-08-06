"""Daily response model."""

from typing import TypedDict

from .place import Place


class DailyForecast(TypedDict):
    """Daily Forecast"""

    daylight: str
    description: str
    skyInfo: int
    skyDesc: str
    temperature: float
    temperatureDesc: str
    comfort: float
    humidity: str
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
    visibility: float
    iconId: int
    iconName: str
    iconLink: str
    weekday: str
    time: str


class DailyForecasts(TypedDict):
    """Daily Forecasts"""

    place: Place
    forecasts: list[DailyForecast]


class DailyResponse(TypedDict):
    """Daily Response"""

    extendedDailyForecasts: list[DailyForecasts]
