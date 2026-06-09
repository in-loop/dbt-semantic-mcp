"""The committed seed CSVs must be exactly what the generator produces."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SEEDS_DIR = REPO_ROOT / "warehouse" / "seeds"


def _load_generator():
    spec = importlib.util.spec_from_file_location(
        "generate_seed", REPO_ROOT / "scripts" / "generate_seed.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["generate_seed"] = module
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_generator_reproduces_committed_seeds(tmp_path: Path) -> None:
    generator = _load_generator()
    generator.main(seeds_dir=tmp_path)
    generated = sorted(p.name for p in tmp_path.glob("*.csv"))
    committed = sorted(p.name for p in SEEDS_DIR.glob("*.csv"))
    assert generated == committed
    for name in generated:
        assert _sha256(tmp_path / name) == _sha256(SEEDS_DIR / name), name
