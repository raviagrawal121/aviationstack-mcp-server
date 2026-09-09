from unittest.mock import AsyncMock

import pytest

from aviationstack_mcp_server.models import Flight
from aviationstack_mcp_server.models.queries import (
    AirportScheduleQuery,
    FlightSearchQuery,
)
from aviationstack_mcp_server.services import FlightService


@pytest.mark.asyncio
async def test_search_flights_returns_typed_flights() -> None:
    client = AsyncMock()

    client.get.return_value = {
        "pagination": {
            "limit": 10,
            "offset": 0,
            "count": 1,
            "total": 1,
        },
        "data": [
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
                    "iata": "JFK",
                },
                "arrival": {
                    "airport": "LAX",
                    "iata": "LAX",
                },
            }
        ],
    }

    service = FlightService(client)

    query = FlightSearchQuery(
        airline_name="Example Airlines",
        limit=10,
    )

    flights = await service.search_flights(query)

    assert len(flights) == 1
    assert isinstance(flights[0], Flight)
    assert flights[0].flight is not None
    assert flights[0].flight.iata == "AA100"

    client.get.assert_awaited_once_with(
        "flights",
        params={
            "limit": 10,
            "airline_name": "Example Airlines",
        },
    )


@pytest.mark.asyncio
async def test_invalid_schedule_type_is_rejected() -> None:
    with pytest.raises(ValueError, match="schedule_type"):
        AirportScheduleQuery(
            airport_iata="JFK",
            schedule_type="invalid",
        )


# from unittest.mock import AsyncMock

# import pytest

# from aviationstack_mcp_server.models import Flight
# from aviationstack_mcp_server.models.queries import (
#     AirportScheduleQuery,
#     FlightSearchQuery,
# )

# from aviationstack_mcp_server.services import FlightService


# @pytest.mark.asyncio
# async def test_search_flights_returns_typed_flights() -> None:
#     client = AsyncMock()

#     client.get.return_value = {
#         "pagination": {
#             "limit": 10,
#             "offset": 0,
#             "count": 1,
#             "total": 1,
#         },
#         "data": [
#             {
#                 "flight_date": "2026-09-08",
#                 "flight_status": "active",
#                 "flight": {
#                     "iata": "AA100",
#                 },
#                 "airline": {
#                     "name": "Example Airlines",
#                     "iata": "AA",
#                 },
#                 "departure": {
#                     "airport": "JFK",
#                     "iata": "JFK",
#                 },
#                 "arrival": {
#                     "airport": "LAX",
#                     "iata": "LAX",
#                 },
#             }
#         ],
#     }

#     service = FlightService(client)

#     flights = await service.search_flights(
#         airline_name="Example Airlines",
#         limit=10,
#     )

#     assert len(flights) == 1
#     assert flights[0].flight is not None
#     assert flights[0].flight.iata == "AA100"

#     client.get.assert_awaited_once_with(
#         "flights",
#         params={
#             "limit": 10,
#             "airline_name": "Example Airlines",
#         },
#     )

# @pytest.mark.asyncio
# async def test_invalid_schedule_type_is_rejected() -> None:
#     client = AsyncMock()

#     service = FlightService(client)

#     with pytest.raises(ValueError, match="schedule_type"):
#         await service.get_airport_schedule(
#             airport_iata="JFK",
#             schedule_type="invalid",
#         )

#     client.get.assert_not_awaited()
