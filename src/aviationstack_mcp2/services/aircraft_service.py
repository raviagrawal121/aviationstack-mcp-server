from __future__ import annotations

import random

from aviationstack_mcp2.client import AviationstackClient
from aviationstack_mcp2.models import (
    AircraftType,
    AircraftTypeResponse,
    Airplane,
    AirplaneResponse,
)
from aviationstack_mcp2.models.queries import RecordLimitQuery


class AircraftService:
    """Application service for aircraft operations."""

    def __init__(self, client: AviationstackClient) -> None:
        self._client = client

    async def list_aircraft_types(
        self,
        query: RecordLimitQuery,
    ) -> list[AircraftType]:
        """Retrieve aircraft type reference data."""

        payload = await self._client.get(
            "aircraft_types",
            params={"limit": query.limit},
        )

        response = AircraftTypeResponse.model_validate(payload)

        return self._sample_records(
            response.data,
            query.limit,
        )

    async def list_airplanes(
        self,
        query: RecordLimitQuery,
    ) -> list[Airplane]:
        """Retrieve airplane reference data."""

        payload = await self._client.get(
            "airplanes",
            params={"limit": query.limit},
        )

        response = AirplaneResponse.model_validate(payload)

        return self._sample_records(
            response.data,
            query.limit,
        )

    @staticmethod
    def _sample_records[T](
        records: list[T],
        requested_count: int,
    ) -> list[T]:
        """Return up to the requested number of randomly sampled records."""

        if not records:
            return []

        return random.sample(
            records,
            min(requested_count, len(records)),
        )

# from __future__ import annotations

# import random

# from aviationstack_mcp2.client import AviationstackClient
# from aviationstack_mcp2.models import (
#     AircraftType,
#     AircraftTypeResponse,
#     Airplane,
#     AirplaneResponse,
# )


# class AircraftService:
#     """Application service for aircraft operations."""

#     def __init__(self, client: AviationstackClient) -> None:
#         self._client = client

#     async def list_aircraft_types(
#         self,
#         *,
#         limit: int = 10,
#     ) -> list[AircraftType]:
#         """Retrieve aircraft type reference data."""

#         payload = await self._client.get(
#             "aircraft_types",
#             params={"limit": limit},
#         )

#         response = AircraftTypeResponse.model_validate(payload)

#         return self._sample_records(
#             response.data,
#             limit,
#         )

#     async def list_airplanes(
#         self,
#         *,
#         limit: int = 10,
#     ) -> list[Airplane]:
#         """Retrieve airplane reference data."""

#         payload = await self._client.get(
#             "airplanes",
#             params={"limit": limit},
#         )

#         response = AirplaneResponse.model_validate(payload)

#         return self._sample_records(
#             response.data,
#             limit,
#         )

#     @staticmethod
#     def _sample_records[T](
#         records: list[T],
#         requested_count: int,
#     ) -> list[T]:
#         if requested_count <= 0:
#             raise ValueError("requested_count must be greater than zero.")

#         return random.sample(
#             records,
#             min(requested_count, len(records)),
#         )