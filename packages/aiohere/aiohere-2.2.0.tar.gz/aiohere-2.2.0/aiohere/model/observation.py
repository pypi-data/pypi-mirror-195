"""Observation response model."""

from typing import TypedDict

from .place import Place


class ObservationForecasts(TypedDict):
    """Observation Forecasts"""

    place: Place
    daylight: str
    description: str
    skyInfo: int
    skyDesc: str
    temperature: float
    temperatureDesc: str
    comfort: float
    highTemperature: float
    lowTemperature: float
    humidity: str
    dewPoint: float
    precipitation1H: int
    precipitationProbability: int
    precipitationDesc: str
    snowFall: float
    windSpeed: float
    windDirection: int
    windDesc: str
    windDescShort: str
    uvIndex: int
    uvDesc: str
    barometerPressure: float
    barometerTrend: str
    visibility: float
    iconId: int
    iconName: str
    iconLink: str
    ageMinutes: int
    activeAlerts: int
    time: str


class ObservationResponse(TypedDict):
    """Observation Response"""

    observations: list[ObservationForecasts]
