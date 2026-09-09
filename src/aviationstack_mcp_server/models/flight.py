from __future__ import annotations

from pydantic import Field

from aviationstack_mcp_server.models.common import AviationstackModel


class FlightIdentifier(AviationstackModel):
    """Flight identification information."""

    iata: str | None = None
    icao: str | None = None
    number: str | None = None


class AirlineReference(AviationstackModel):
    """Airline information associated with a flight."""

    name: str | None = None
    iata: str | None = None
    icao: str | None = None


class AirportReference(AviationstackModel):
    """Airport information associated with a flight."""

    airport: str | None = None
    iata: str | None = None
    icao: str | None = None
    timezone: str | None = None
    terminal: str | None = None
    gate: str | None = None

    scheduled: str | None = None
    estimated: str | None = None
    actual: str | None = None
    delay: int | None = None


class FlightAircraftReference(AviationstackModel):
    """Aircraft information associated with a flight."""

    registration: str | None = None
    iata: str | None = None
    icao: str | None = None
    model: str | None = None
    model_code: str | None = None
    model_text: str | None = Field(
        default=None,
        alias="modelText",
    )


class Flight(AviationstackModel):
    """Aviationstack flight record."""

    flight_date: str | None = None
    flight_status: str | None = None

    flight: FlightIdentifier | None = None
    airline: AirlineReference | None = None
    departure: AirportReference | None = None
    arrival: AirportReference | None = None
    aircraft: FlightAircraftReference | None = None


class FlightResponse(AviationstackModel):
    """Aviationstack response containing flight records."""

    pagination: dict | None = None
    data: list[Flight] = Field(default_factory=list)


class ScheduleFlightIdentifier(AviationstackModel):
    """Flight identifier returned by timetable endpoints."""

    iata_number: str | None = Field(
        default=None,
        alias="iataNumber",
    )
    icao_number: str | None = Field(
        default=None,
        alias="icaoNumber",
    )


class ScheduleTimeReference(AviationstackModel):
    """Schedule timing information."""

    estimated_time: str | None = Field(
        default=None,
        alias="estimatedTime",
    )
    scheduled_time: str | None = Field(
        default=None,
        alias="scheduledTime",
    )
    actual_time: str | None = Field(
        default=None,
        alias="actualTime",
    )
    iata_code: str | None = Field(
        default=None,
        alias="iataCode",
    )
    terminal: str | None = None
    gate: str | None = None
    delay: int | None = None


class ScheduleFlight(AviationstackModel):
    """Flight record returned by timetable/future schedule endpoints."""

    airline: AirlineReference | None = None
    flight: ScheduleFlightIdentifier | None = None
    departure: ScheduleTimeReference | None = None
    arrival: ScheduleTimeReference | None = None
    aircraft: FlightAircraftReference | None = None


class ScheduleResponse(AviationstackModel):
    """Response containing scheduled flights."""

    pagination: dict | None = None
    data: list[ScheduleFlight] = Field(default_factory=list)
