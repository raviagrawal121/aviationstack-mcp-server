from aviationstack_mcp2.models import (
    Airport,
    Flight,
    ScheduleFlight,
)


def test_flight_model_parses_nested_data() -> None:
    flight = Flight.model_validate(
        {
            "flight_date": "2026-09-08",
            "flight_status": "active",
            "flight": {
                "iata": "AA100",
            },
            "airline": {
                "name": "Example Airlines",
                "iata": "AA",
            },
            "departure": {
                "airport": "JFK",
                "timezone": "America/New_York",
                "scheduled": "2026-09-08T10:00:00+00:00",
                "delay": 5,
            },
            "arrival": {
                "airport": "LAX",
                "timezone": "America/Los_Angeles",
            },
        }
    )

    assert flight.flight is not None
    assert flight.flight.iata == "AA100"

    assert flight.airline is not None
    assert flight.airline.name == "Example Airlines"

    assert flight.departure is not None
    assert flight.departure.airport == "JFK"
    assert flight.departure.delay == 5


def test_airport_model_accepts_reference_data() -> None:
    airport = Airport.model_validate(
        {
            "airport_name": "John F Kennedy International",
            "iata_code": "JFK",
            "icao_code": "KJFK",
            "country_iso2": "US",
            "timezone": "America/New_York",
        }
    )

    assert airport.iata_code == "JFK"
    assert airport.icao_code == "KJFK"


def test_schedule_model_supports_api_field_aliases() -> None:
    schedule = ScheduleFlight.model_validate(
        {
            "flight": {
                "iataNumber": "AA100",
            },
            "departure": {
                "scheduledTime": "2026-09-08T10:00:00+00:00",
                "estimatedTime": "2026-09-08T10:10:00+00:00",
                "iataCode": "JFK",
            },
        }
    )

    assert schedule.flight is not None
    assert schedule.flight.iata_number == "AA100"

    assert schedule.departure is not None
    assert schedule.departure.scheduled_time is not None
    assert schedule.departure.iata_code == "JFK"
