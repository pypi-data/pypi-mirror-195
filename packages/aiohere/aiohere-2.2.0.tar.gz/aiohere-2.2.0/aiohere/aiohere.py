"""A module to query the here web api."""
from __future__ import annotations

import asyncio
import socket
from typing import Any, Mapping, MutableMapping
from .model.astronomy import AstronomyResponse
from .model.daily import DailyResponse
from .model.daily_simple import DailySimpleResponse
from .model.hourly import HourlyResponse
from .model.observation import ObservationResponse
from .model.response import HereWeatherResponse

import aiohttp
import async_timeout
from yarl import URL

from .model.product_types import WeatherProductType

from .exceptions import (
    HereError,
    HereInvalidRequestError,
    HereTimeOutError,
    HereUnauthorizedError,
)

SCHEME = "https"
API_HOST = "weather.hereapi.com"
API_PATH = "/v3/report"
API_URL = str(URL.build(scheme=SCHEME, host=API_HOST, path=API_PATH))


class AioHere:
    """Main class for handling connections with here."""

    def __init__(
        self,
        api_key: str,
        request_timeout: int = 10,
        session: aiohttp.client.ClientSession | None = None,
    ) -> None:
        """Initialize connection with here.
        Class constructor for setting up an AioHere object to
        communicate with the here API.
        Args:
            api_key: HERE API key.
            request_timeout: Max timeout to wait for a response from the API.
            session: Optional, shared, aiohttp client session.
        """
        self._session = session
        self._close_session = False

        self.api_key = api_key
        self.request_timeout = request_timeout

    async def request(
        self,
        method: str = "GET",
        data: Any | None = None,
        json_data: dict | None = None,
        params: Mapping[str, str] | None = None,
    ) -> Any:
        """Handle a request to the weenect API.
        Make a request against the weenect API and handles the response.
        Args:
            uri: The request URI on the weenect API to call.
            method: HTTP method to use for the request; e.g., GET, POST.
            data: RAW HTTP request data to send with the request.
            json_data: Dictionary of data to send as JSON with the request.
            params: Mapping of request parameters to send with the request.
        Returns:
            The response from the API. In case the response is a JSON response,
            the method will return a decoded JSON response as a Python
            dictionary.
        Raises:
            WeenectConnectionError: An error occurred while communicating
                with the weenect API (connection issues).
            WeenectHomeError: An error occurred while processing the
                response from the weenect API (invalid data).
        """

        headers = {
            "Accept": "application/json",
            "DNT": "1",
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    method,
                    API_URL,
                    data=data,
                    json=json_data,
                    params=params,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            raise HereTimeOutError(
                "Timeout occurred while connecting to the here API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise HereError(
                "Error occurred while communicating with the here API."
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if response.status // 100 in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise get_error_from_response(await response.json())
            raise HereError(response.status, {"message": contents.decode("utf8")})

        if response.status == 204:  # NO CONTENT
            response.close()
            return None

        if "application/json" in content_type:
            return await response.json()

    async def weather_for_coordinates(
        self,
        latitude: float,
        longitude: float,
        products: list[WeatherProductType],
        one_observation: bool = True,
        metric: bool = True,
        language: str = "en-US",
    ) -> AstronomyResponse | DailySimpleResponse | DailyResponse | HourlyResponse | ObservationResponse:
        """Request the product for given location name.
        Args:
          latitude (float):
            Latitude.
          longitude (float):
            Longitude.
          products (WeatherProductType):
            A list of WeatherProductType identifying the types of reports to obtain.
          one_observation (bool):
            Limit the result to the best mapped weather station.
          metric (bool):
            Use the metric system.
          language (str):
            Language of the descriptions to return.
        Returns:
          DestinationWeatherResponse
        Raises:
          HereError
        """

        params: MutableMapping[str, str] = {
            "apiKey": self.api_key,
            "products": ",".join(p.value for p in products),
            "units": "metric" if metric is True else "imperial",
            "location": f"{latitude},{longitude}",
            "lang": str(language),
        }
        if WeatherProductType.OBSERVATION in products:
            params["oneObservation"] = "true" if one_observation is True else "false"
        json_data: HereWeatherResponse = await self.request(params=params)
        return json_data["places"][0]

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> AioHere:
        """Async enter.
        Returns:
            The AioHere object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.
        Args:
            _exc_info: Exec type.
        """
        await self.close()


def get_error_from_response(json_data: Mapping[str, Any]) -> HereError:
    """Return the correct error type."""
    if "error" in json_data:
        if json_data["error"] == "Unauthorized":
            return HereUnauthorizedError(json_data["error_description"])
    error_type = json_data.get("title")
    error_message = json_data.get("cause")
    if error_type == "Invalid Request":
        return HereInvalidRequestError(error_message)
    return HereError(error_message)
