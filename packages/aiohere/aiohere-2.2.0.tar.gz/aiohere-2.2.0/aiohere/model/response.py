"""Response models for here."""
from __future__ import annotations

from typing import TypedDict

from .daily import DailyResponse
from .hourly import HourlyResponse
from .observation import ObservationResponse
from .daily_simple import DailySimpleResponse
from .astronomy import AstronomyResponse


class HereWeatherResponse(TypedDict):
    """Base Response"""

    places: list[
        AstronomyResponse
        | DailySimpleResponse
        | DailyResponse
        | HourlyResponse
        | ObservationResponse
    ]
