from datetime import date

import pytest
from pydantic import ValidationError

from aviationstack_mcp2.models import (
    AirportScheduleQuery,
    FlightSearchQuery,
    HistoricalFlightQuery,
    ScheduleType,
)


def test_flight_query_normalizes_iata_codes() -> None:
    query = FlightSearchQuery(
        departure_iata=" jfk ",
        arrival_iata="lax",
        limit=5,
    )

    assert query.departure_iata == "JFK"
    assert query.arrival_iata == "LAX"


def test_historical_query_parses_date() -> None:
    query = HistoricalFlightQuery(
        flight_date="2026-09-08",
    )

    assert query.flight_date == date(2026, 9, 8)


def test_schedule_type_is_enum() -> None:
    query = AirportScheduleQuery(
        airport_iata="jfk",
        schedule_type="arrival",
    )

    assert query.airport_iata == "JFK"
    assert query.schedule_type is ScheduleType.ARRIVAL


def test_invalid_schedule_type_is_rejected() -> None:
    with pytest.raises(ValidationError):
        AirportScheduleQuery(
            airport_iata="JFK",
            schedule_type="invalid",
        )


def test_limit_cannot_exceed_boundary() -> None:
    with pytest.raises(ValidationError):
        FlightSearchQuery(limit=101)


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        FlightSearchQuery(
            airline_name="Example",
            unsupported_field="value",
        )
