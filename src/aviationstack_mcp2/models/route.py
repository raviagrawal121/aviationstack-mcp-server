from __future__ import annotations

from pydantic import Field

from aviationstack_mcp2.models.common import AviationstackModel


class Route(AviationstackModel):
    """Airline route reference data."""

    airline_iata: str | None = None
    airline_icao: str | None = None
    flight_number: str | None = None
    dep_iata: str | None = None
    dep_icao: str | None = None
    arr_iata: str | None = None
    arr_icao: str | None = None


class RouteResponse(AviationstackModel):
    """Response containing routes."""

    pagination: dict | None = None
    data: list[Route] = Field(default_factory=list)
