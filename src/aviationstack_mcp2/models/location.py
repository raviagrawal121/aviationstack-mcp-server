from __future__ import annotations

from pydantic import Field

from aviationstack_mcp2.models.common import AviationstackModel


class Country(AviationstackModel):
    """Country reference data."""

    name: str | None = None
    capital: str | None = None
    currency_code: str | None = None
    fips_code: str | None = None
    country_iso2: str | None = None
    country_iso3: str | None = None
    continent: str | None = None
    country_id: str | None = None
    currency_name: str | None = None
    country_iso_numeric: str | None = None
    phone_prefix: str | None = None
    population: int | None = None


class CountryResponse(AviationstackModel):
    """Response containing countries."""

    pagination: dict | None = None
    data: list[Country] = Field(default_factory=list)


class City(AviationstackModel):
    """City reference data."""

    gmt: str | None = None
    city_id: str | None = None
    iata_code: str | None = None
    country_iso2: str | None = None
    geoname_id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    city_name: str | None = None


class CityResponse(AviationstackModel):
    """Response containing cities."""

    pagination: dict | None = None
    data: list[City] = Field(default_factory=list)
