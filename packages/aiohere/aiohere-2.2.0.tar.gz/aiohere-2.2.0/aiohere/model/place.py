"""Place model"""

from typing import TypedDict


class Address(TypedDict):
    """Address"""

    countryCode: str
    countryName: str
    state: str
    city: str


class Location(TypedDict):
    """GPS Location"""

    lat: float
    lng: float


class Place(TypedDict):
    """Place"""

    address: Address
    location: Location
