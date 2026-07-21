"""Find the ray-workshop repo root (JupyterLab cwd is usually extras/notebooks)."""

from __future__ import annotations

from pathlib import Path

_REPO_MARKER = Path("extras/scripts/scale_data.py")


def setup_workshop_path() -> Path:
    """Return repo root for ``runtime_env.working_dir``."""
    import os

    for env_name in ("RAY_WORKSHOP_REPO", "REPO_ROOT"):
        env_val = os.environ.get(env_name)
        if env_val:
            root = Path(env_val).expanduser().resolve()
            if (root / _REPO_MARKER).is_file():
                return root

    for directory in [Path.cwd(), *Path.cwd().parents]:
        root = directory.resolve()
        if (root / _REPO_MARKER).is_file():
            return root

    raise FileNotFoundError(
        "Could not find ray-workshop (expected extras/scripts/scale_data.py). "
        "Clone the repo into your workbench or set RAY_WORKSHOP_REPO."
    )
