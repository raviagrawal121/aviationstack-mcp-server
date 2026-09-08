from mcp.server.mcpserver import Context

from aviationstack_mcp2.mcp.dependencies import AppContext
from aviationstack_mcp2.models.queries import (
    RecordLimitQuery,
    RouteSearchQuery,
    TaxSearchQuery,
)


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

        return await app.services.reference.list_countries(query)

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

        return await app.services.reference.list_cities(query)

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

        return await app.services.reference.search_routes(query)

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

        return await app.services.reference.search_taxes(query)