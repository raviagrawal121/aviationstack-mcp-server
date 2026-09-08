from .aircraft import (
    AircraftType,
    AircraftTypeResponse,
    Airplane,
    AirplaneResponse,
)
from .airline import Airline, AirlineResponse
from .airport import Airport, AirportResponse
from .common import AviationstackModel, AviationstackResponse
from .flight import (
    AirlineReference,
    AirportReference,
    Flight,
    FlightAircraftReference,
    FlightIdentifier,
    FlightResponse,
    ScheduleFlight,
    ScheduleFlightIdentifier,
    ScheduleResponse,
    ScheduleTimeReference,
)
from .location import City, CityResponse, Country, CountryResponse
from .route import Route, RouteResponse
from .tax import Tax, TaxResponse

from .queries import (
    AirlineSearchQuery,
    AirportScheduleQuery,
    AirportSearchQuery,
    FlightSearchQuery,
    FutureScheduleQuery,
    HistoricalFlightQuery,
    PaginationQuery,
    QueryModel,
    RecordLimitQuery,
    RouteSearchQuery,
    ScheduleType,
    TaxSearchQuery,
)

__all__ = [
    "AircraftType",
    "AircraftTypeResponse",
    "Airline",
    "AirlineReference",
    "AirlineResponse",
    "Airport",
    "AirportReference",
    "AirportResponse",
    "AviationstackModel",
    "AviationstackResponse",
    "Airplane",
    "AirplaneResponse",
    "City",
    "CityResponse",
    "Country",
    "CountryResponse",
    "Flight",
    "FlightAircraftReference",
    "FlightIdentifier",
    "FlightResponse",
    "Route",
    "RouteResponse",
    "ScheduleFlight",
    "ScheduleFlightIdentifier",
    "ScheduleResponse",
    "ScheduleTimeReference",
    "Tax",
    "TaxResponse",
    "AirlineSearchQuery",
    "AirportScheduleQuery",
    "AirportSearchQuery",
    "FlightSearchQuery",
    "FutureScheduleQuery",
    "HistoricalFlightQuery",
    "PaginationQuery",
    "QueryModel",
    "RecordLimitQuery",
    "RouteSearchQuery",
    "ScheduleType",
    "TaxSearchQuery",
]