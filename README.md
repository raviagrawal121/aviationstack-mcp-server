# Aviationstack MCP Server

MCP server providing aviation data through the Aviationstack API.

## Development

```bash
uv sync
source .venv/bin/activate
```

Normal tests are offline and do not require an Aviationstack API key:

```bash
uv run pytest -m "not live_api"
```

Run the live MCP-to-Aviationstack test explicitly with `AVIATIONSTACK_API_KEY`
set in the environment or `.env`:

```bash
uv run pytest -m live_api
```

Probe endpoint access for the configured account, using one bounded request per
capability:

```bash
AVIATIONSTACK_LIVE=1 uv run pytest -m capability_discovery -s
```