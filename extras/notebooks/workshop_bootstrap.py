"""Stdlib-only path setup for workshop notebooks (no codeflare import)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_MARKER = Path("extras/scripts/scale_data.py")


def setup_workshop_path() -> Path:
    """Find repo root from JupyterLab cwd (usually .../ray-workshop/extras/notebooks)."""
    for env_name in ("RAY_WORKSHOP_REPO", "REPO_ROOT"):
        env_val = __import__("os").environ.get(env_name)
        if env_val:
            root = Path(env_val).expanduser().resolve()
            if (root / _REPO_MARKER).is_file():
                _insert_helper(root)
                return root

    for directory in [Path.cwd(), *Path.cwd().parents]:
        root = directory.resolve()
        if (root / _REPO_MARKER).is_file():
            _insert_helper(root)
            return root

    raise FileNotFoundError(
        "Could not find ray-workshop (expected extras/scripts/scale_data.py). "
        "Clone the repo into your workbench or set RAY_WORKSHOP_REPO."
    )


def _insert_helper(root: Path) -> None:
    helper = str(root / "extras/python")
    if helper not in sys.path:
        sys.path.insert(0, helper)
