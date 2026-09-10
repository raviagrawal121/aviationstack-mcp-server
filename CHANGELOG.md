# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows Semantic Versioning.

## [0.1.0] - 2026-09-10

### Added

- Initial public release of the Aviationstack MCP server.
- MCP tools for:
  - Flight search
  - Historical flight search
  - Flight schedules
  - Airport search
  - Airline search
  - Aircraft types
  - Airplanes
  - Countries
  - Cities
  - Routes
  - Taxes
- MCP prompts for:
  - Flight search planning
  - Schedule search planning
  - Reference-data search planning
- MCP resources for server metadata and documentation.
- Typed Pydantic models for API requests and responses.
- Asynchronous HTTP client using `httpx`.
- Retry handling for transient HTTP failures.
- Typed Aviationstack error hierarchy.
- Configuration through environment variables.
- Structured application logging.
- Correlation IDs and request timing.
- Security controls for API-key handling and secret redaction.
- Unit and MCP integration test coverage.
- Separate opt-in live API tests.
- PyPI packaging with wheel and source distribution.
- `uvx aviationstack-mcp-server` execution support.
- GitHub Actions CI and release workflows.
- TestPyPI and production PyPI publishing through Trusted Publishing.

[0.1.0]: https://github.com/raviagrawal121/aviationstack-mcp-server/releases/tag/v0.1.0