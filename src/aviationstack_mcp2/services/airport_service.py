from __future__ import annotations

from aviationstack_mcp2.client import AviationstackClient
from aviationstack_mcp2.models import Airport, AirportResponse
from aviationstack_mcp2.models.queries import AirportSearchQuery


class AirportService:
    """Application service for airport operations."""

    def __init__(self, client: AviationstackClient) -> None:
        self._client = client

    async def search_airports(
        self,
        query: AirportSearchQuery,
    ) -> list[Airport]:
        """Search airports with pagination."""

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
            "airports",
            params=params,
        )

        response = AirportResponse.model_validate(payload)

        return response.data


# from __future__ import annotations

# from aviationstack_mcp2.client import AviationstackClient
# from aviationstack_mcp2.models import Airport, AirportResponse
# from aviationstack_mcp2.models.queries import AirportSearchQuery


# class AirportService:
#     """Application service for airport operations."""

#     def __init__(self, client: AviationstackClient) -> None:
#         self._client = client

#     async def search_airports(
#             self,
#             query: AirportSearchQuery,
#             ) -> list[Airport]:

#         params = {
#             "limit": query.limit,
#             "offset": query.offset,
#             "search": query.search,
#         }

#         params = {
#             key: value
#             for key, value in params.items()
#             if value is not None
#         }

#         payload = await self._client.get(
#             "airports",
#             params=params,
#         )

#         response = AirportResponse.model_validate(payload)

#         return response.data

#     # async def search_airports(
#     #     self,
#     #     *,
#     #     search: str | None = None,
#     #     limit: int = 10,
#     #     offset: int = 0,
#     # ) -> list[Airport]:
#     #     """Search airports with pagination."""

#     #     params: dict[str, str | int] = {
#     #         "limit": limit,
#     #         "offset": offset,
#     #     }

#     #     if search:
#     #         params["search"] = search

#     #     payload = await self._client.get(
#     #         "airports",
#     #         params=params,
#     #     )

#     #     response = AirportResponse.model_validate(payload)

#     #     return response.data