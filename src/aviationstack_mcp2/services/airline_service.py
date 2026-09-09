from __future__ import annotations

import logging

from aviationstack_mcp2.client import AviationstackClient
from aviationstack_mcp2.models import Airline, AirlineResponse
from aviationstack_mcp2.models.queries import AirlineSearchQuery

logger = logging.getLogger(__name__)


class AirlineService:
    """Application service for airline operations."""

    def __init__(self, client: AviationstackClient) -> None:
        self._client = client

    async def search_airlines(
        self,
        query: AirlineSearchQuery,
    ) -> list[Airline]:
        """Search airlines with pagination."""

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

        logger.info(
            "Searching airlines: limit=%s offset=%s search_provided=%s",
            query.limit,
            query.offset,
            query.search is not None,
        )

        payload = await self._client.get(
            "airlines",
            params=params,
        )

        response = AirlineResponse.model_validate(payload)
        logger.debug(
            "Airline search complete: fetched=%s",
            len(response.data),
        )

        return response.data






# from __future__ import annotations

# from aviationstack_mcp2.client import AviationstackClient
# from aviationstack_mcp2.models import Airline, AirlineResponse


# class AirlineService:
#     """Application service for airline operations."""

#     def __init__(self, client: AviationstackClient) -> None:
#         self._client = client

#     async def search_airlines(
#         self,
#         *,
#         search: str | None = None,
#         limit: int = 10,
#         offset: int = 0,
#     ) -> list[Airline]:
#         """Search airlines with pagination."""

#         params: dict[str, str | int] = {
#             "limit": limit,
#             "offset": offset,
#         }

#         if search:
#             params["search"] = search

#         payload = await self._client.get(
#             "airlines",
#             params=params,
#         )

#         response = AirlineResponse.model_validate(payload)

#         return response.data