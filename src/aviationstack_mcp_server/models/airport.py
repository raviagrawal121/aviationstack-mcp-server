from __future__ import annotations

from pydantic import Field

from aviationstack_mcp_server.models.common import AviationstackModel


class Airport(AviationstackModel):
    """Airport reference data."""

    airport_name: str | None = None
    iata_code: str | None = None
    icao_code: str | None = None
    city_iata_code: str | None = None
    country_name: str | None = None
    country_iso2: str | None = None
    timezone: str | None = None
    gmt: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    airport_id: str | None = Field(
        default=None,
        alias="airport_id",
    )


class AirportResponse(AviationstackModel):
    """Aviationstack airport response."""

    pagination: dict | None = None
    data: list[Airport] = Field(default_factory=list)
