import logging

from mcp.server.mcpserver import MCPServer

logger = logging.getLogger(__name__)


def register_metadata_resources(server: MCPServer) -> None:
    """Register server metadata resources."""

    logger.debug("Registering Aviationstack server metadata resource")

    @server.resource(
        "aviationstack://metadata/server",
        name="server_metadata",
        title="Aviationstack MCP Server Metadata",
        description=(
            "Metadata describing the Aviationstack MCP server, "
            "its capabilities, and supported MCP primitives."
        ),
        mime_type="application/json",
    )
    def server_metadata() -> dict[str, object]:
        """Return public server metadata."""

        logger.debug("Reading metadata resource: aviationstack://metadata/server")
        return {
            "name": "aviationstack-mcp",
            "project": "aviationstack_mcp2",
            "description": (
                "MCP server providing structured access to "
                "Aviationstack flight and aviation reference data."
            ),
            "capabilities": {
                "tools": True,
                "prompts": True,
                "resources": True,
            },
            "domains": [
                "flights",
                "airports",
                "airlines",
                "aircraft",
                "reference_data",
            ],
        }
