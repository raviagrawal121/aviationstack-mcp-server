from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class AviationstackModel(BaseModel):
    """Base model for Aviationstack API data."""

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )


class AviationstackResponse(AviationstackModel):
    """Generic envelope returned by Aviationstack."""

    pagination: dict[str, Any] | None = None
