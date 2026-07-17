"""Find the ray-workshop repo root and shared ClusterConfiguration defaults."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codeflare_sdk import ClusterConfiguration

_REPO_MARKER = Path("extras/scripts/scale_data.py")


def setup_workshop_path() -> Path:
    """Return repo root (JupyterLab cwd is usually .../ray-workshop/extras/notebooks)."""
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


def workshop_cluster_configuration(
    name: str,
    namespace: str,
    local_queue: str,
) -> ClusterConfiguration:
    """Default workshop RayCluster: 2 workers × 1 GPU each.

    Head has no GPU request (omit nvidia.com/gpu: 0 — that can suspend admission).
    """
    from codeflare_sdk import ClusterConfiguration

    return ClusterConfiguration(
        name=name,
        namespace=namespace,
        local_queue=local_queue,
        num_workers=2,
        head_cpu_requests=5,
        head_cpu_limits=8,
        head_memory_requests=4,
        head_memory_limits=8,
        worker_cpu_requests=1,
        worker_cpu_limits=2,
        worker_extended_resource_requests={"nvidia.com/gpu": 1},
        worker_memory_requests=4,
        worker_memory_limits=6,
        write_to_file=False,
    )
