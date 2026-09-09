import logging

from mcp.server.mcpserver import Context

from aviationstack_mcp_server.mcp.dependencies import AppContext
from aviationstack_mcp_server.mcp.errors import mcp_error_boundary
from aviationstack_mcp_server.models.queries import RecordLimitQuery

logger = logging.getLogger(__name__)


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
    @mcp_error_boundary
    async def list_aircraft_types(
        query: RecordLimitQuery,
        ctx: Context[AppContext],
    ):
        """List aircraft type records."""

        app = ctx.request_context.lifespan_context
        logger.info("MCP tool called: list_aircraft_types limit=%s", query.limit)
        records = await app.services.aircraft.list_aircraft_types(query)
        logger.debug(
            "MCP tool completed: list_aircraft_types returned=%s",
            len(records),
        )

        return records

    @server.tool(
        name="list_airplanes",
        title="List Airplanes",
        description=(
            "List individual airplane records available from "
            "Aviationstack. Use the limit parameter to control "
            "the number of records."
        ),
    )
    @mcp_error_boundary
    async def list_airplanes(
        query: RecordLimitQuery,
        ctx: Context[AppContext],
    ):
        """List individual airplane records."""

        app = ctx.request_context.lifespan_context
        logger.info("MCP tool called: list_airplanes limit=%s", query.limit)
        records = await app.services.aircraft.list_airplanes(query)
        logger.debug(
            "MCP tool completed: list_airplanes returned=%s",
            len(records),
        )

        return records
