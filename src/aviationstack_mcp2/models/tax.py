from __future__ import annotations

from pydantic import Field

from aviationstack_mcp2.models.common import AviationstackModel


class Tax(AviationstackModel):
    """Aviation tax reference data."""

    tax_id: str | None = None
    tax_name: str | None = None
    iata_code: str | None = None


class TaxResponse(AviationstackModel):
    """Response containing aviation taxes."""

    pagination: dict | None = None
    data: list[Tax] = Field(default_factory=list)