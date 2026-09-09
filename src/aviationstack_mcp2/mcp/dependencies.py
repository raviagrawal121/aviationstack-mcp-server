import logging
from dataclasses import dataclass

from aviationstack_mcp2.client.aviationstack import AviationstackClient
from aviationstack_mcp2.services.aircraft_service import AircraftService
from aviationstack_mcp2.services.airline_service import AirlineService
from aviationstack_mcp2.services.airport_service import AirportService
from aviationstack_mcp2.services.flight_service import FlightService
from aviationstack_mcp2.services.reference_service import ReferenceDataService

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ServiceContainer:
    """Application-level collection of domain services."""

    flight: FlightService
    airport: AirportService
    airline: AirlineService
    aircraft: AircraftService
    reference: ReferenceDataService


@dataclass(frozen=True, slots=True)
class AppContext:
    """Application dependencies shared across MCP requests."""

    client: AviationstackClient
    services: ServiceContainer


def build_services(
    client: AviationstackClient,
) -> ServiceContainer:
    """Build all domain services using a shared API client."""

    services = ServiceContainer(
        flight=FlightService(client),
        airport=AirportService(client),
        airline=AirlineService(client),
        aircraft=AircraftService(client),
        reference=ReferenceDataService(client),
    )
    logger.debug(
        "Application services built: names=%s",
        ("flight", "airport", "airline", "aircraft", "reference"),
    )

    return services


def build_app_context(
    client: AviationstackClient,
) -> AppContext:
    """Build the application dependency container."""

    services = build_services(client)
    logger.debug("Application dependency context built")

    return AppContext(
        client=client,
        services=services,
    )
