"""The MCP tool layer answers from the governed definitions — cross-checked
against direct SQL on the same DuckDB file."""

from __future__ import annotations

import duckdb
import pytest

from dbt_semantic_mcp import warehouse

EXPECTED_METRICS = {
    "revenue",
    "units_sold",
    "gross_profit",
    "order_count",
    "average_order_value",
    "new_customers",
    "on_time_shipments",
    "shipped_orders",
    "on_time_shipment_rate",
}


def test_list_metrics_catalog() -> None:
    catalog = warehouse.list_metrics()
    assert {m["name"] for m in catalog} == EXPECTED_METRICS
    revenue = next(m for m in catalog if m["name"] == "revenue")
    assert "customer__region" in revenue["group_bys"]
    assert "metric_time" in revenue["group_bys"]
    assert revenue["description"]


def test_query_revenue_matches_direct_sql() -> None:
    rows = warehouse.query_metrics(["revenue"])
    assert len(rows) == 1
    metric_value = float(rows[0]["revenue"])

    db = warehouse.warehouse_dir() / "target" / "warehouse.duckdb"
    with duckdb.connect(str(db), read_only=True) as conn:
        result = conn.execute("select sum(line_revenue) from fct_order_items").fetchone()
    assert result is not None
    assert abs(metric_value - float(result[0])) < 0.01


def test_query_metric_grouped_by_region() -> None:
    rows = warehouse.query_metrics(["order_count"], group_by=["customer__region"])
    regions = {r["customer__region"] for r in rows}
    assert regions == {"midwest", "northeast", "south", "west"}


def test_query_unknown_metric_raises() -> None:
    with pytest.raises(warehouse.WarehouseError, match="mf query failed"):
        warehouse.query_metrics(["not_a_metric"])


def test_lineage_for_model_and_metric() -> None:
    model = warehouse.describe_lineage("fct_orders")
    assert "stg_orders" in model["upstream"]
    assert "int_order_items_pricing" in model["upstream"]

    metric = warehouse.describe_lineage("revenue")
    assert metric["resolved_node"] == "fct_order_items"
    assert "int_order_items_pricing" in metric["upstream"]


def test_lineage_unknown_node_raises() -> None:
    with pytest.raises(warehouse.WarehouseError, match="no dbt node"):
        warehouse.describe_lineage("not_a_node")
