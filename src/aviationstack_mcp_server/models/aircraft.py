from __future__ import annotations

from pydantic import Field

from aviationstack_mcp_server.models.common import AviationstackModel


class AircraftType(AviationstackModel):
    """Aircraft type reference data."""

    aircraft_name: str | None = None
    iata_code: str | None = None
    icao_code: str | None = None


class AircraftTypeResponse(AviationstackModel):
    """Response containing aircraft types."""

    pagination: dict | None = None
    data: list[AircraftType] = Field(default_factory=list)


class Airplane(AviationstackModel):
    """Detailed airplane information."""

    production_line: str | None = None
    plane_owner: str | None = None
    plane_age: int | float | None = None
    model_name: str | None = None
    model_code: str | None = None
    plane_series: str | None = None
    registration_number: str | None = None
    engines_type: str | None = None
    engines_count: int | None = None
    delivery_date: str | None = None
    first_flight_date: str | None = None


class AirplaneResponse(AviationstackModel):
    """Response containing airplane records."""

    pagination: dict | None = None
    data: list[Airplane] = Field(default_factory=list)
