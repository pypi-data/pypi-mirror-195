"""Hourly response model."""

from typing import TypedDict

from .place import Place


class HourlyForecast(TypedDict):
    """Hourly Forecast"""

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
    visibility: float
    iconId: int
    iconName: str
    iconLink: str
    weekday: str
    time: str


class HourlyForecasts(TypedDict):
    """Hourly Forecasts"""

    place: Place
    forecasts: list[HourlyForecast]


class HourlyResponse(TypedDict):
    """Hourly Response"""

    hourlyForecasts: list[HourlyForecasts]
