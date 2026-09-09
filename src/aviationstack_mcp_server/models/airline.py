from __future__ import annotations

from pydantic import Field

from aviationstack_mcp_server.models.common import AviationstackModel


class Airline(AviationstackModel):
    """Airline reference data."""

    airline_name: str | None = None
    iata_code: str | None = None
    icao_code: str | None = None
    callsign: str | None = None
    status: str | None = None
    country_name: str | None = None
    country_iso2: str | None = None

    airline_id: str | None = Field(
        default=None,
        alias="airline_id",
    )


class AirlineResponse(AviationstackModel):
    """Aviationstack airline response."""

    pagination: dict | None = None
    data: list[Airline] = Field(default_factory=list)
