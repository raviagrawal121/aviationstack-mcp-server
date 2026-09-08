from mcp.server.mcpserver import MCPServer


def register_metadata_resources(server: MCPServer) -> None:
    """Register server metadata resources."""

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