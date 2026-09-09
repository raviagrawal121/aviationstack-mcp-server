from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from aviationstack_mcp2.client import AviationstackClient, HTTPClient
from aviationstack_mcp2.config import Settings
from aviationstack_mcp2.errors import (
    AviationstackAPIError,
    AviationstackAuthenticationError,
    AviationstackAuthorizationError,
    AviationstackRateLimitError,
)


@dataclass(frozen=True)
class EndpointCapability:
    name: str
    endpoint: str
    params: dict[str, object]


@dataclass(frozen=True)
class CapabilityResult:
    name: str
    endpoint: str
    status: str
    error_code: str | None = None


CAPABILITIES = (
    EndpointCapability("real_time_flights", "flights", {"limit": 1}),
    EndpointCapability(
        "airports",
        "airports",
        {"search": "London", "limit": 1},
    ),
    EndpointCapability("airlines", "airlines", {"limit": 1}),
    EndpointCapability("airplanes", "airplanes", {"limit": 1}),
    EndpointCapability("aircraft_types", "aircraft_types", {"limit": 1}),
    EndpointCapability("cities", "cities", {"limit": 1}),
    EndpointCapability("countries", "countries", {"limit": 1}),
    EndpointCapability("taxes", "taxes", {"limit": 1}),
    EndpointCapability("routes", "routes", {"limit": 1}),
    EndpointCapability(
        "historical_flights",
        "flights",
        {"flight_date": (date.today() - timedelta(days=1)).isoformat(), "limit": 1},
    ),
    EndpointCapability(
        "timetable",
        "timetable",
        {"iataCode": "LHR", "type": "departure"},
    ),
    EndpointCapability(
        "future_flights",
        "flightsFuture",
        {
            "iataCode": "LHR",
            "type": "departure",
            "date": (date.today() + timedelta(days=7)).isoformat(),
        },
    ),
)


def _require_live_configuration() -> Settings:
    if os.getenv("AVIATIONSTACK_LIVE") != "1":
        pytest.skip("Set AVIATIONSTACK_LIVE=1 to run capability discovery.")

    try:
        return Settings()
    except ValidationError:
        pytest.skip("Set AVIATIONSTACK_API_KEY to run capability discovery.")


def _classify_error(error: Exception) -> tuple[str, str | None]:
    if isinstance(error, AviationstackAuthenticationError):
        return "AUTHENTICATION_FAILED", error.error_code
    if isinstance(error, AviationstackAuthorizationError):
        return "RESTRICTED", error.error_code
    if isinstance(error, AviationstackRateLimitError):
        return "RATE_LIMITED", error.error_code
    if isinstance(error, AviationstackAPIError):
        if error.error_code == "function_access_restricted":
            return "RESTRICTED", error.error_code
        return "API_ERROR", error.error_code
    return "ERROR", None


@pytest.mark.live_api
@pytest.mark.capability_discovery
@pytest.mark.asyncio
async def test_discover_aviationstack_capabilities() -> None:
    """Discover which API functions the configured account can access."""

    settings = _require_live_configuration()
    http_client = HTTPClient(settings)
    client = AviationstackClient(settings, http_client)
    results: list[CapabilityResult] = []

    try:
        for capability in CAPABILITIES:
            try:
                await client.get(capability.endpoint, params=capability.params)
            except Exception as exc:
                status, error_code = _classify_error(exc)
                results.append(
                    CapabilityResult(
                        capability.name,
                        capability.endpoint,
                        status,
                        error_code,
                    )
                )
            else:
                results.append(
                    CapabilityResult(
                        capability.name,
                        capability.endpoint,
                        "AVAILABLE",
                    )
                )
    finally:
        await client.close()

    print("Aviationstack capability discovery:")
    for result in results:
        suffix = f" error_code={result.error_code}" if result.error_code else ""
        print(f"  {result.name}: {result.status} endpoint=/{result.endpoint}{suffix}")

    assert len(results) == len(CAPABILITIES)
    assert all(result.status != "ERROR" for result in results)
