import logging

import pytest

from aviationstack_mcp2.logging_config import CorrelationIdFilter
from aviationstack_mcp2.mcp.errors import mcp_error_boundary
from aviationstack_mcp2.observability import (
    generate_correlation_id,
    get_correlation_id,
    set_correlation_id,
)


def test_generate_correlation_id() -> None:
    value = generate_correlation_id()

    assert value
    assert len(value) == 32


def test_correlation_id_context() -> None:
    try:
        set_correlation_id("abc123")

        assert get_correlation_id() == "abc123"
    finally:
        set_correlation_id("")


def test_logging_filter_adds_correlation_id() -> None:
    try:
        set_correlation_id("abc123")
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="hello",
            args=(),
            exc_info=None,
        )

        assert CorrelationIdFilter().filter(record) is True
        assert record.correlation_id == "abc123"
    finally:
        set_correlation_id("")


@pytest.mark.asyncio
async def test_tool_boundary_logs_one_correlation_id(
) -> None:
    @mcp_error_boundary
    async def operation() -> str:
        return "ok"

    records: list[logging.LogRecord] = []

    class RecordHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            records.append(record)

    handler = RecordHandler()
    handler.addFilter(CorrelationIdFilter())
    tool_logger = logging.getLogger("aviationstack_mcp2.mcp.errors")
    tool_logger.addHandler(handler)
    tool_logger.setLevel(logging.INFO)

    try:
        set_correlation_id("")
        assert await operation() == "ok"
    finally:
        tool_logger.removeHandler(handler)

    assert len(records) == 2
    assert records[0].correlation_id
    assert records[0].correlation_id != "-"
    assert records[0].correlation_id == records[1].correlation_id
    assert get_correlation_id() == ""
