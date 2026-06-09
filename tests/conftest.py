from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from dbt_semantic_mcp import warehouse

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def built_warehouse() -> Path:
    """Build the warehouse once if its artifacts are missing."""
    wh = warehouse.warehouse_dir()
    needed = [
        wh / "target" / "warehouse.duckdb",
        wh / "target" / "manifest.json",
        wh / "target" / "semantic_manifest.json",
    ]
    if not all(p.exists() for p in needed):
        dbt = shutil.which("dbt")
        assert dbt is not None, "dbt not on PATH"
        subprocess.run([dbt, "build"], cwd=wh, check=True, timeout=600)
    return wh
