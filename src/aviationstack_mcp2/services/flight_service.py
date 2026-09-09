from __future__ import annotations

import logging
import random
from typing import TypeVar

from aviationstack_mcp2.client import AviationstackClient
from aviationstack_mcp2.models import (
    Flight,
    FlightResponse,
    ScheduleFlight,
    ScheduleResponse,
)
from aviationstack_mcp2.models.queries import (
    AirportScheduleQuery,
    FlightSearchQuery,
    FutureScheduleQuery,
    HistoricalFlightQuery,
)

logger = logging.getLogger(__name__)
T = TypeVar("T")


class FlightService:
    """Application service for flight-related operations."""

    def __init__(self, client: AviationstackClient) -> None:
        self._client = client

    async def search_flights(
        self,
        query: FlightSearchQuery,
    ) -> list[Flight]:
        """Search live flights using supported Aviationstack filters."""

        params = {
            "limit": query.limit,
            "airline_name": query.airline_name,
            "airline_iata": query.airline_iata,
            "flight_iata": query.flight_iata,
            "flight_icao": query.flight_icao,
            "dep_iata": query.departure_iata,
            "arr_iata": query.arrival_iata,
        }

        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        logger.info(
            "Searching live flights: limit=%s filters=%s",
            query.limit,
            sorted(key for key in params if key != "limit"),
        )

        payload = await self._client.get(
            "flights",
            params=params,
        )

        response = FlightResponse.model_validate(payload)
        logger.debug("Live flight search complete: fetched=%s", len(response.data))

        return response.data

    async def get_historical_flights(
        self,
        query: HistoricalFlightQuery,
    ) -> list[Flight]:
        """Retrieve historical flights for a specific date."""

        params = {
            "flight_date": query.flight_date.isoformat(),
            "airline_iata": query.airline_iata,
            "dep_iata": query.departure_iata,
            "arr_iata": query.arrival_iata,
            "limit": query.limit,
        }

        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        logger.info(
            "Searching historical flights: date=%s limit=%s filters=%s",
            query.flight_date,
            query.limit,
            sorted(key for key in params if key not in {"flight_date", "limit"}),
        )

        payload = await self._client.get(
            "flights",
            params=params,
        )

        response = FlightResponse.model_validate(payload)
        logger.debug(
            "Historical flight search complete: fetched=%s",
            len(response.data),
        )

        return response.data

    async def get_airport_schedule(
        self,
        query: AirportScheduleQuery,
    ) -> list[ScheduleFlight]:
        """Retrieve current airport arrival or departure schedules."""

        params = {
            "iataCode": query.airport_iata,
            "type": query.schedule_type.value,
            "airline_name": query.airline_name,
        }

        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        logger.info(
            "Getting airport schedule: airport=%s type=%s airline_filter=%s",
            query.airport_iata,
            query.schedule_type.value,
            query.airline_name is not None,
        )

        payload = await self._client.get(
            "timetable",
            params=params,
        )

        response = ScheduleResponse.model_validate(payload)
        records = self._sample_records(response.data, query.limit)
        logger.debug(
            "Airport schedule retrieval complete: fetched=%s returned=%s",
            len(response.data),
            len(records),
        )

        return records

    async def get_future_schedule(
        self,
        query: FutureScheduleQuery,
    ) -> list[ScheduleFlight]:
        """Retrieve future airport arrival or departure schedules."""

        params = {
            "iataCode": query.airport_iata,
            "type": query.schedule_type.value,
            "date": query.date.isoformat(),
            "airline_iata": query.airline_iata,
        }

        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        logger.info(
            "Getting future schedule: airport=%s date=%s type=%s airline_filter=%s",
            query.airport_iata,
            query.date,
            query.schedule_type.value,
            query.airline_iata is not None,
        )

        payload = await self._client.get(
            "flightsFuture",
            params=params,
        )

        response = ScheduleResponse.model_validate(payload)
        records = self._sample_records(response.data, query.limit)
        logger.debug(
            "Future schedule retrieval complete: fetched=%s returned=%s",
            len(response.data),
            len(records),
        )

        return records

    @staticmethod
    def _sample_records(
        records: list[T],
        requested_count: int,
    ) -> list[T]:
        """Return up to the requested number of randomly sampled records."""

        if requested_count <= 0:
            raise ValueError("requested_count must be greater than zero.")

        if not records:
            return []

        return random.sample(
            records,
            min(requested_count, len(records)),
        )


# from __future__ import annotations

# import random

# from aviationstack_mcp2.models.queries import (
#     FlightSearchQuery,
#     HistoricalFlightQuery,
#     AirportScheduleQuery,
# )
# from aviationstack_mcp2.client import AviationstackClient

# from aviationstack_mcp2.models import (
#     Flight,
#     FlightResponse,
#     ScheduleFlight,
#     ScheduleResponse,
# )


# class FlightService:
#     """Application service for flight-related operations."""

#     def __init__(self, client: AviationstackClient) -> None:
#         self._client = client

#     async def search_flights(        
#         self,
#         query: FlightSearchQuery,
#     ) -> list[Flight]:
#         """Search live flights using supported Aviationstack filters."""

#         params = {
#             "limit": query.limit,
#             "airline_name": query.airline_name,
#             "airline_iata": query.airline_iata,
#             "flight_iata": query.flight_iata,
#             "flight_icao": query.flight_icao,
#             "dep_iata": query.departure_iata,
#             "arr_iata": query.arrival_iata,
#         }


#         params = {
#             key: value
#             for key, value in params.items()
#             if value is not None
#         }

#         payload = await self._client.get(
#             "flights",
#             params=params,
#         )

#         response = FlightResponse.model_validate(payload)

#         return response.data

#     async def get_historical_flights(
#         self,
#         query: HistoricalFlightQuery,
#     ) -> list[Flight]:
#         """Retrieve historical flights for a specific date."""

#         params = {
#         "flight_date": query.flight_date.isoformat(),
#         "airline_iata": query.airline_iata,
#         "dep_iata": query.departure_iata,
#         "arr_iata": query.arrival_iata,
#         "limit": query.limit,
#         }

#         params = {
#         key: value
#         for key, value in params.items()
#         if value is not None
#         }

#         payload = await self._client.get(
#             "flights",
#             params=params,
#         )

#         response = FlightResponse.model_validate(payload)

#         return response.data

#     async def get_airport_schedule(
#         self,
#         query: AirportScheduleQuery,
#     ) -> list[ScheduleFlight]:
#         """Retrieve current airport arrival or departure schedules."""

#         params = {
#         "iataCode": query.airport_iata,
#         "type": query.schedule_type.value,
#         "airline_name": query.airline_name,
#         }

#         params = {
#             key: value
#             for key, value in params.items()
#             if value is not None
#         }

#         payload = await self._client.get(
#             "timetable",
#             params=params,
#         )

#         response = ScheduleResponse.model_validate(payload)

#         return self._sample_records(
#             response.data,
#             query.limit,
#         )

    

#     async def get_future_schedule(
#         self,
#         *,
#         airport_iata: str,
#         schedule_type: str,
#         date: str,
#         airline_iata: str | None = None,
#         limit: int = 10,
#     ) -> list[ScheduleFlight]:
#         """Retrieve future airport arrival or departure schedules."""

#         normalized_type = schedule_type.strip().lower()

#         if normalized_type not in {"arrival", "departure"}:
#             raise ValueError(
#                 "schedule_type must be either 'arrival' or 'departure'."
#             )

#         params: dict[str, str | int] = {
#             "iataCode": airport_iata,
#             "type": normalized_type,
#             "date": date,
#         }

#         if airline_iata:
#             params["airline_iata"] = airline_iata

#         payload = await self._client.get(
#             "flightsFuture",
#             params=params,
#         )

#         response = ScheduleResponse.model_validate(payload)

#         return self._sample_records(
#             response.data,
#             limit,
#         )

#     @staticmethod
#     def _sample_records[T](
#         records: list[T],
#         requested_count: int,
#     ) -> list[T]:
#         """Return up to the requested number of randomly sampled records."""

#         if requested_count <= 0:
#             raise ValueError("requested_count must be greater than zero.")

#         if not records:
#             return []

#         return random.sample(
#             records,
#             min(requested_count, len(records)),
#         )