from typing import Any


class FakeAviationstackClient:
    """Fake API client for MCP integration tests."""

    def __init__(self) -> None:
        self.closed = False

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if endpoint == "airports":
            return {
                "data": [
                    {
                        "airport_name": "Indira Gandhi International Airport",
                        "iata_code": "DEL",
                        "icao_code": "VIDP",
                        "city_iata_code": "DEL",
                        "country_iso2": "IN",
                    }
                ]
            }

        raise AssertionError(f"Unexpected endpoint in test: {endpoint}")

    async def close(self) -> None:
        self.closed = True
