# Aviationstack MCP Server

[![CI](https://github.com/raviagrawal121/aviationstack-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/raviagrawal121/aviationstack-mcp-server/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/aviationstack-mcp-server.svg)](https://pypi.org/project/aviationstack-mcp-server/)
[![Python](https://img.shields.io/pypi/pyversions/aviationstack-mcp-server.svg)](https://pypi.org/project/aviationstack-mcp-server/)
[![License](https://img.shields.io/pypi/l/aviationstack-mcp-server.svg)](https://github.com/raviagrawal121/aviationstack-mcp-server/blob/main/LICENSE)

An MCP server that gives AI assistants structured access to flight, airport,
airline, aircraft, route, tax, and other aviation reference data from the
[Aviationstack API](https://aviationstack.com/).

## Features

- Search current and historical flight records.
- Search airports and airlines.
- Retrieve airport arrival and departure schedules.
- Browse aircraft types, airplanes, countries, and cities.
- Search routes and aviation taxes.
- Expose planning prompts and machine-readable MCP resources.
- Validate query input with typed Pydantic models.
- Return safe MCP-facing errors without leaking internal details.

## Requirements

- Python 3.13 or newer for local development.
- An Aviationstack API key for live requests.
- An MCP-compatible client, such as Claude Desktop, Cursor, or another MCP host.

## Installation

Run directly with `uvx`:

```bash
uvx aviationstack-mcp-server
```

Set your Aviationstack API key in the environment:

```bash
export AVIATIONSTACK_API_KEY="your-api-key"
```

The server reads the key when it starts. It does not require a local checkout
or a manually managed virtual environment for normal MCP client use.

## Configuration

The required setting is:

| Environment variable | Required | Default | Description |
| --- | --- | --- | --- |
| `AVIATIONSTACK_API_KEY` | Yes | None | API key used for Aviationstack requests. |

Optional settings include:

| Environment variable | Default | Description |
| --- | --- | --- |
| `AVIATIONSTACK_BASE_URL` | `https://api.aviationstack.com/v1` | Aviationstack API base URL. |
| `ENVIRONMENT` | `development` | Application environment: `development`, `testing`, `staging`, or `production`. |
| `LOG_LEVEL` | `INFO` | Logging level, such as `DEBUG`, `INFO`, or `WARNING`. |
| `AVIATIONSTACK_CONNECT_TIMEOUT` | `5.0` | HTTP connection timeout in seconds. |
| `AVIATIONSTACK_READ_TIMEOUT` | `30.0` | HTTP read timeout in seconds. |
| `AVIATIONSTACK_WRITE_TIMEOUT` | `30.0` | HTTP write timeout in seconds. |
| `AVIATIONSTACK_POOL_TIMEOUT` | `5.0` | HTTP connection-pool timeout in seconds. |
| `AVIATIONSTACK_RETRY_MAX_ATTEMPTS` | `3` | Maximum number of HTTP attempts. |
| `AVIATIONSTACK_RETRY_BACKOFF_FACTOR` | `0.5` | Exponential retry backoff factor. |

For local development, create a `.env` file in the repository root. Do not
commit it:

```dotenv
AVIATIONSTACK_API_KEY=your-api-key
```

## MCP Client Configuration

Add the server to an MCP client using the `uvx` command:

```json
{
  "mcpServers": {
    "aviationstack": {
      "command": "uvx",
      "args": [
        "aviationstack-mcp-server"
      ],
      "env": {
        "AVIATIONSTACK_API_KEY": "your-api-key"
      }
    }
  }
}
```

The exact location of this configuration depends on the MCP client. Keep the
API key in the client's environment configuration rather than putting it in
tool arguments or prompts.

## Available Tools

Every tool accepts a structured `query` object. Unless noted otherwise,
`limit` defaults to `10` and must be between `1` and `100`. IATA codes are
normalized to uppercase by the server.

| Tool | Description | Parameters |
| --- | --- | --- |
| `search_flights` | Search current scheduled flight records. | `airline_name` (optional string); `airline_iata` (optional 2-3 character code); `flight_iata` (optional string); `flight_icao` (optional string); `departure_iata` (optional 3-character code); `arrival_iata` (optional 3-character code); `limit` (optional integer, 1-100). |
| `search_historical_flights` | Search historical flight records for a specific date. | `flight_date` (required `YYYY-MM-DD` date); `airline_iata` (optional 2-3 character code); `departure_iata` (optional 3-character code); `arrival_iata` (optional 3-character code); `limit` (optional integer, 1-100). |
| `get_flight_schedule` | Retrieve airport arrival or departure schedules. | `airport_iata` (required 3-character code); `schedule_type` (required `arrival` or `departure`); `airline_name` (optional string); `limit` (optional integer, 1-100). |
| `search_airports` | Search airport records by name, city, or other text. | `search` (optional string); `limit` (optional integer, 1-100, default `10`); `offset` (optional integer, default `0`). |
| `search_airlines` | Search airline records by name or other text. | `search` (optional string); `limit` (optional integer, 1-100, default `10`); `offset` (optional integer, default `0`). |
| `list_aircraft_types` | List aircraft type records. | `limit` (optional integer, 1-100, default `10`). |
| `list_airplanes` | List individual airplane records. | `limit` (optional integer, 1-100, default `10`). |
| `list_countries` | List country reference records. | `limit` (optional integer, 1-100, default `10`). |
| `list_cities` | List city reference records. | `limit` (optional integer, 1-100, default `10`). |
| `search_routes` | Search airline routes by airline and airports. | `airline_iata` (optional 2-3 character code); `departure_iata` (optional 3-character code); `arrival_iata` (optional 3-character code); `limit` (optional integer, 1-100, default `10`); `offset` (optional integer, default `0`). |
| `search_taxes` | Search aviation tax records. | `search` (optional string); `limit` (optional integer, 1-100, default `10`); `offset` (optional integer, default `0`). |

Examples of structured tool arguments:

```json
{
  "query": {
    "departure_iata": "DEL",
    "arrival_iata": "DXB",
    "limit": 10
  }
}
```

```json
{
  "query": {
    "airport_iata": "LHR",
    "schedule_type": "departure",
    "limit": 20
  }
}
```

## Available Prompts

| Prompt | Arguments | Purpose |
| --- | --- | --- |
| `plan_flight_search` | `request` (string) | Translate a natural-language flight request into appropriate flight filters. |
| `plan_schedule_search` | `airport` (string), `schedule_type` (string, default `departure`) | Plan an airport arrival or departure schedule lookup. |
| `plan_reference_data_search` | `request` (string) | Choose and plan the appropriate reference-data lookup tool. |

## Available Resources

| Resource URI | Description |
| --- | --- |
| `aviationstack://metadata/server` | Server identity, capabilities, and supported aviation domains. |
| `aviationstack://metadata/endpoints` | Aviationstack endpoint and operation mapping. |
| `aviationstack://documentation/tools` | Machine-readable documentation for the exposed tools. |

## Development

Clone the repository and install the development environment with `uv`:

```bash
git clone https://github.com/raviagrawal121/aviationstack-mcp-server.git
cd aviationstack-mcp-server
uv sync
source .venv/bin/activate
```

Run the server locally after setting `AVIATIONSTACK_API_KEY`:

```bash
uv run aviationstack-mcp-server
```

Build the source distribution and wheel:

```bash
uv build
```

## Testing

The default test suite is offline. MCP integration tests inject an in-memory
Aviationstack client, so they do not require an API key or network access:

```bash
uv run pytest -m "not live_api and not capability_discovery"
```

To run only the MCP integration tests:

```bash
uv run pytest tests/integration/mcp
```

Lint the project with Ruff:

```bash
uv run ruff check .
```

## Live API Testing

Live tests make real requests and require an Aviationstack API key:

```bash
export AVIATIONSTACK_API_KEY="your-api-key"
uv run pytest -m live_api
```

Capability discovery is opt-in and probes supported endpoint access for the
configured account. It makes bounded requests against the live API:

```bash
AVIATIONSTACK_LIVE=1 uv run pytest -m capability_discovery -s
```

Run live tests only when network access and API quota are available. The
results depend on the Aviationstack plan associated with the configured key.

## Architecture

The server is organized into a small set of layers:

```text
MCP client
    |
MCP tools, prompts, and resources
    |
Application context and domain services
    |
Aviationstack API client and HTTP transport
    |
Aviationstack REST API
```

- `src/aviationstack_mcp_server/mcp/` registers the MCP surface and manages the
  application lifespan.
- `src/aviationstack_mcp_server/services/` contains domain operations for
  flights, airports, airlines, aircraft, and reference data.
- `src/aviationstack_mcp_server/client/` contains the API client, HTTP
  transport, retries, and client factory.
- `src/aviationstack_mcp_server/models/` contains typed response and query
  models.
- Non-live MCP tests inject a fake client through `create_server(client_factory=...)`;
  production uses the default factory, which loads `Settings` and the API key.

## Contributing

1. Create a focused branch for your change.
2. Add or update tests for behavior changes.
3. Run the offline test suite and Ruff locally.
4. Update the README when the public MCP surface changes.
5. Open a pull request with a concise description of the change.

Please do not include API keys, `.env` files, build artifacts, or live API
responses containing sensitive data in commits or pull requests.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
