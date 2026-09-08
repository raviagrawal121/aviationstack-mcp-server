from __future__ import annotations

import random

from aviationstack_mcp2.client import AviationstackClient
from aviationstack_mcp2.models import (
    City,
    CityResponse,
    Country,
    CountryResponse,
    Route,
    RouteResponse,
    Tax,
    TaxResponse,
)
from aviationstack_mcp2.models.queries import (
    RecordLimitQuery,
    RouteSearchQuery,
    TaxSearchQuery,
)


class ReferenceDataService:
    """Application service for Aviationstack reference data."""

    def __init__(self, client: AviationstackClient) -> None:
        self._client = client

    async def list_countries(
        self,
        query: RecordLimitQuery,
    ) -> list[Country]:
        """Retrieve country reference data."""

        payload = await self._client.get(
            "countries",
            params={"limit": query.limit},
        )

        response = CountryResponse.model_validate(payload)

        return self._sample_records(
            response.data,
            query.limit,
        )

    async def list_cities(
        self,
        query: RecordLimitQuery,
    ) -> list[City]:
        """Retrieve city reference data."""

        payload = await self._client.get(
            "cities",
            params={"limit": query.limit},
        )

        response = CityResponse.model_validate(payload)

        return self._sample_records(
            response.data,
            query.limit,
        )

    async def search_routes(
        self,
        query: RouteSearchQuery,
    ) -> list[Route]:
        """Search airline routes."""

        params = {
            "limit": query.limit,
            "offset": query.offset,
            "airline_iata": query.airline_iata,
            "dep_iata": query.departure_iata,
            "arr_iata": query.arrival_iata,
        }

        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        payload = await self._client.get(
            "routes",
            params=params,
        )

        response = RouteResponse.model_validate(payload)

        return response.data

    async def search_taxes(
        self,
        query: TaxSearchQuery,
    ) -> list[Tax]:
        """Search aviation taxes."""

        params = {
            "limit": query.limit,
            "offset": query.offset,
            "search": query.search,
        }

        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        payload = await self._client.get(
            "taxes",
            params=params,
        )

        response = TaxResponse.model_validate(payload)

        return response.data

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
# from aviationstack_mcp2.models.queries import RouteSearchQuery
# from aviationstack_mcp2.models import (
#     City,
#     CityResponse,
#     Country,
#     CountryResponse,
#     Route,
#     RouteResponse,
#     Tax,
#     TaxResponse,
# )


# class ReferenceDataService:
#     """Application service for Aviationstack reference data."""

#     def __init__(self, client: AviationstackClient) -> None:
#         self._client = client

#     async def list_countries(
#         self,
#         *,
#         limit: int = 10,
#     ) -> list[Country]:
#         """Retrieve country reference data."""

#         payload = await self._client.get(
#             "countries",
#             params={"limit": limit},
#         )

#         response = CountryResponse.model_validate(payload)

#         return self._sample_records(response.data, limit)

#     async def list_cities(
#         self,
#         *,
#         limit: int = 10,
#     ) -> list[City]:
#         """Retrieve city reference data."""

#         payload = await self._client.get(
#             "cities",
#             params={"limit": limit},
#         )

#         response = CityResponse.model_validate(payload)

#         return self._sample_records(response.data, limit)

#     async def search_routes(self,query: RouteSearchQuery,) -> list[Route]:

#         params = {
#             "limit": query.limit,
#             "offset": query.offset,
#             "airline_iata": query.airline_iata,
#             "dep_iata": query.departure_iata,
#             "arr_iata": query.arrival_iata,
#         }

#         params = {
#             key: value
#             for key, value in params.items()
#             if value is not None
#         }

#         payload = await self._client.get(
#             "routes",
#             params=params,
#         )

#         response = RouteResponse.model_validate(payload)

#         return response.data

#     # async def search_routes(
#     #     self,
#     #     *,
#     #     airline_iata: str | None = None,
#     #     departure_iata: str | None = None,
#     #     arrival_iata: str | None = None,
#     #     limit: int = 10,
#     #     offset: int = 0,
#     # ) -> list[Route]:
#     #     """Search airline routes."""

#     #     params: dict[str, str | int] = {
#     #         "limit": limit,
#     #         "offset": offset,
#     #     }

#     #     filters = {
#     #         "airline_iata": airline_iata,
#     #         "dep_iata": departure_iata,
#     #         "arr_iata": arrival_iata,
#     #     }

#     #     params.update(
#     #         {
#     #             key: value
#     #             for key, value in filters.items()
#     #             if value
#     #         }
#     #     )

#     #     payload = await self._client.get(
#     #         "routes",
#     #         params=params,
#     #     )

#     #     response = RouteResponse.model_validate(payload)

#     #     return response.data

#     async def search_taxes(
#         self,
#         *,
#         search: str | None = None,
#         limit: int = 10,
#         offset: int = 0,
#     ) -> list[Tax]:
#         """Search aviation taxes."""

#         params: dict[str, str | int] = {
#             "limit": limit,
#             "offset": offset,
#         }

#         if search:
#             params["search"] = search

#         payload = await self._client.get(
#             "taxes",
#             params=params,
#         )

#         response = TaxResponse.model_validate(payload)

#         return response.data

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