from mcp.server.mcpserver import Context

from aviationstack_mcp2.mcp.dependencies import AppContext
from aviationstack_mcp2.models.queries import RecordLimitQuery


def register_aircraft_tools(server) -> None:
    """Register aircraft-related MCP tools."""

    @server.tool(
        name="list_aircraft_types",
        title="List Aircraft Types",
        description=(
            "List aircraft type records available from Aviationstack. "
            "Use the limit parameter to control the number of records."
        ),
    )
    async def list_aircraft_types(
        query: RecordLimitQuery,
        ctx: Context[AppContext],
    ):
        """List aircraft type records."""

        app = ctx.request_context.lifespan_context

        return await app.services.aircraft.list_aircraft_types(query)

    @server.tool(
        name="list_airplanes",
        title="List Airplanes",
        description=(
            "List individual airplane records available from "
            "Aviationstack. Use the limit parameter to control "
            "the number of records."
        ),
    )
    async def list_airplanes(
        query: RecordLimitQuery,
        ctx: Context[AppContext],
    ):
        """List individual airplane records."""

        app = ctx.request_context.lifespan_context

        return await app.services.aircraft.list_airplanes(query)