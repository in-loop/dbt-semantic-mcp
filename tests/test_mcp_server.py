"""End-to-end: a real MCP client over stdio gets a metric back."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

REPO_ROOT = Path(__file__).resolve().parents[1]


async def _roundtrip() -> tuple[list[str], list[dict[str, Any]]]:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "dbt_semantic_mcp.server"],
        cwd=str(REPO_ROOT),
    )
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        result = await session.call_tool(
            "query_metric",
            {"metrics": ["revenue"], "group_by": ["metric_time__year"]},
        )
        assert not result.isError
        rows: list[dict[str, Any]] = []
        for content in result.content:
            assert content.type == "text"
            parsed: Any = json.loads(content.text)
            if isinstance(parsed, list):
                rows.extend(dict(r) for r in parsed)  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
            else:
                rows.append(parsed)
        return [t.name for t in tools.tools], rows


def test_stdio_roundtrip_returns_revenue_rows() -> None:
    tool_names, rows = asyncio.run(asyncio.wait_for(_roundtrip(), timeout=120))
    assert set(tool_names) == {"list_metrics", "query_metric", "describe_lineage"}
    assert len(rows) == 2  # 2024 and 2025
    assert all(float(r["revenue"]) > 0 for r in rows)
