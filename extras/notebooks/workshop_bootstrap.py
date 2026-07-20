"""Find the ray-workshop repo root and shared ClusterConfiguration defaults."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codeflare_sdk import Cluster, ClusterConfiguration

_REPO_MARKER = Path("extras/scripts/scale_data.py")

# Shared across Topics 1–3 so participants reuse one RayCluster.
WORKSHOP_CLUSTER_NAME = "ray-workshop"


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


def ensure_workshop_cluster(
    namespace: str,
    local_queue: str,
    name: str = WORKSHOP_CLUSTER_NAME,
) -> Cluster:
    """Attach to an existing workshop RayCluster, or create one.

    Topics 1–3 share ``ray-workshop``. ``apply()`` updates if present, creates
    if missing. Tear down only at the end of Topic 3 (or when stuck).
    """
    from codeflare_sdk import Cluster, get_cluster

    try:
        cluster = get_cluster(cluster_name=name, namespace=namespace)
        print(f"Attached to existing cluster {name!r} in {namespace!r}")
    except Exception as exc:  # noqa: BLE001 — SDK raises various miss errors
        print(f"No existing cluster {name!r} ({exc}); creating with workshop defaults")
        cluster = Cluster(
            workshop_cluster_configuration(
                name=name,
                namespace=namespace,
                local_queue=local_queue,
            )
        )

    cluster.apply()
    cluster.wait_ready()
    return cluster
