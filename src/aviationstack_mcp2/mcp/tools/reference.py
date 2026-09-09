import logging

from mcp.server.mcpserver import Context

from aviationstack_mcp2.mcp.dependencies import AppContext
from aviationstack_mcp2.models.queries import (
    RecordLimitQuery,
    RouteSearchQuery,
    TaxSearchQuery,
)

logger = logging.getLogger(__name__)


def register_reference_tools(server) -> None:
    """Register reference-data MCP tools."""

    @server.tool(
        name="list_countries",
        title="List Countries",
        description=(
            "List country records available from Aviationstack. "
            "Use the limit parameter to control the number of records."
        ),
    )
    async def list_countries(
        query: RecordLimitQuery,
        ctx: Context[AppContext],
    ):
        """List country reference records."""

        app = ctx.request_context.lifespan_context
        logger.info("MCP tool called: list_countries limit=%s", query.limit)
        records = await app.services.reference.list_countries(query)
        logger.debug(
            "MCP tool completed: list_countries returned=%s",
            len(records),
        )

        return records

    @server.tool(
        name="list_cities",
        title="List Cities",
        description=(
            "List city records available from Aviationstack. "
            "Use the limit parameter to control the number of records."
        ),
    )
    async def list_cities(
        query: RecordLimitQuery,
        ctx: Context[AppContext],
    ):
        """List city reference records."""

        app = ctx.request_context.lifespan_context
        logger.info("MCP tool called: list_cities limit=%s", query.limit)
        records = await app.services.reference.list_cities(query)
        logger.debug(
            "MCP tool completed: list_cities returned=%s",
            len(records),
        )

        return records

    @server.tool(
        name="search_routes",
        title="Search Routes",
        description=(
            "Search airline route records using supported route "
            "filters such as airline, departure airport, arrival "
            "airport, and pagination."
        ),
    )
    async def search_routes(
        query: RouteSearchQuery,
        ctx: Context[AppContext],
    ):
        """Search route records."""

        app = ctx.request_context.lifespan_context
        logger.info(
            "MCP tool called: search_routes limit=%s offset=%s filters=%s",
            query.limit,
            query.offset,
            [
                field
                for field in ("airline_iata", "departure_iata", "arrival_iata")
                if getattr(query, field) is not None
            ],
        )
        records = await app.services.reference.search_routes(query)
        logger.debug(
            "MCP tool completed: search_routes returned=%s",
            len(records),
        )

        return records

    @server.tool(
        name="search_taxes",
        title="Search Taxes",
        description=(
            "Search aviation tax records using supported tax "
            "filters and pagination."
        ),
    )
    async def search_taxes(
        query: TaxSearchQuery,
        ctx: Context[AppContext],
    ):
        """Search tax records."""

        app = ctx.request_context.lifespan_context
        logger.info(
            "MCP tool called: search_taxes limit=%s offset=%s search_provided=%s",
            query.limit,
            query.offset,
            query.search is not None,
        )
        records = await app.services.reference.search_taxes(query)
        logger.debug(
            "MCP tool completed: search_taxes returned=%s",
            len(records),
        )

        return records