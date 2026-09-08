from __future__ import annotations

from datetime import date as Date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class QueryModel(BaseModel):
    """Base model for application query/input objects."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class PaginationQuery(QueryModel):
    """Common pagination parameters."""

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of records to return.",
    )

    offset: int = Field(
        default=0,
        ge=0,
        description="Number of records to skip.",
    )


class ScheduleType(StrEnum):
    """Supported airport schedule types."""

    ARRIVAL = "arrival"
    DEPARTURE = "departure"

class FlightSearchQuery(QueryModel):
    """Parameters for searching live flights."""

    airline_name: str | None = Field(
        default=None,
        description="Airline name, such as Delta Air Lines.",
    )

    airline_iata: str | None = Field(
        default=None,
        min_length=2,
        max_length=3,
        description="Airline IATA code, such as DL.",
    )

    flight_iata: str | None = Field(
        default=None,
        description="Flight IATA number, such as DL123.",
    )

    flight_icao: str | None = Field(
        default=None,
        description="Flight ICAO identifier.",
    )

    departure_iata: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
        description="Departure airport IATA code.",
    )

    arrival_iata: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
        description="Arrival airport IATA code.",
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    @field_validator(
        "airline_iata",
        "departure_iata",
        "arrival_iata",
        mode="before",
    )
    @classmethod
    def normalize_iata_code(cls, value: str | None) -> str | None:
        """Normalize IATA codes to uppercase."""

        if value is None:
            return None

        return value.strip().upper()

class HistoricalFlightQuery(QueryModel):
    """Parameters for historical flight searches."""

    flight_date: Date = Field(
        description="Flight date in YYYY-MM-DD format.",
    )

    airline_iata: str | None = Field(
        default=None,
        min_length=2,
        max_length=3,
    )

    departure_iata: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    arrival_iata: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    @field_validator(
        "airline_iata",
        "departure_iata",
        "arrival_iata",
        mode="before",
    )
    @classmethod
    def normalize_iata_code(cls, value: str | None) -> str | None:
        """Normalize IATA codes."""

        if value is None:
            return None

        return value.strip().upper()


class AirportScheduleQuery(QueryModel):
    """Parameters for airport arrival/departure schedule queries."""

    airport_iata: str = Field(
        min_length=3,
        max_length=3,
        description="Airport IATA code.",
    )

    schedule_type: ScheduleType = Field(
        description="Whether to retrieve arrival or departure schedules.",
    )

    airline_name: str | None = Field(
        default=None,
        description="Optional airline name filter.",
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    @field_validator("airport_iata", mode="before")
    @classmethod
    def normalize_airport_code(cls, value: str) -> str:
        """Normalize airport IATA code."""

        return value.strip().upper()


class FutureScheduleQuery(QueryModel):
    """Parameters for future airport schedule queries."""

    airport_iata: str = Field(
        min_length=3,
        max_length=3,
        description="Airport IATA code.",
    )

    schedule_type: ScheduleType

    date: Date = Field(
        description="Future schedule date.",
    )

    airline_iata: str | None = Field(
        default=None,
        min_length=2,
        max_length=3,
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    @field_validator("airport_iata", mode="before")
    @classmethod
    def normalize_airport_code(cls, value: str) -> str:
        return value.strip().upper()


class AirportSearchQuery(PaginationQuery):
    """Parameters for airport searches."""

    search: str | None = Field(
        default=None,
        description="Airport name, city, or other search text.",
    )

class AirlineSearchQuery(PaginationQuery):
    """Parameters for airline searches."""

    search: str | None = Field(
        default=None,
        description="Airline search text.",
    )

class RouteSearchQuery(PaginationQuery):
    """Parameters for route searches."""

    airline_iata: str | None = Field(
        default=None,
        min_length=2,
        max_length=3,
    )

    departure_iata: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    arrival_iata: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    @field_validator(
        "airline_iata",
        "departure_iata",
        "arrival_iata",
        mode="before",
    )
    @classmethod
    def normalize_codes(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip().upper()

class TaxSearchQuery(PaginationQuery):
    """Parameters for tax searches."""

    search: str | None = Field(
        default=None,
        description="Tax name or code search text.",
    )

class RecordLimitQuery(QueryModel):
    """Query for bounded reference-data retrieval."""

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )