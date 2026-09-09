from aviationstack_mcp_server.config import get_settings
from aviationstack_mcp_server.logging_config import configure_logging
from aviationstack_mcp_server.mcp.server import create_server


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
