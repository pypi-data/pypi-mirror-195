"""Astronomy response model."""

from typing import TypedDict

from .place import Place


class AstronomyForecast(TypedDict):
    """Astronomy Forecast"""

    sunRise: str
    sunSet: str
    moonRise: str
    moonSet: str
    moonPhase: str
    moonPhaseDescription: str
    iconName: str
    time: str


class AstronomyForecasts(TypedDict):
    """Astronomy Forecasts"""

    place: Place
    forecasts: list[AstronomyForecast]


class AstronomyResponse(TypedDict):
    """Astronomy Response"""

    astronomyForecasts: list[AstronomyForecasts]
