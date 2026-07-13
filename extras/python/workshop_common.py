"""Shared helpers aligned with OpenShift AI 3.4 distributed workloads docs."""

from __future__ import annotations

import os
import time
from pathlib import Path

from codeflare_sdk import ManagedClusterConfig, TokenAuthentication
from codeflare_sdk import RayJob  # noqa: F401 — re-exported for notebooks
from codeflare_sdk import list_local_queues  # noqa: F401 — re-exported for notebooks

NAMESPACE = os.environ.get("RAY_WORKSHOP_NAMESPACE", "ray-workshop")
LOCAL_QUEUE = os.environ.get("RAY_WORKSHOP_LOCAL_QUEUE", "ray-workshop-queue")

_REPO_MARKER = Path("extras/scripts/scale_data.py")


def repo_root() -> Path:
    """Find the ray-workshop clone (JupyterLab cwd is often the notebook directory)."""
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

    for candidate in (Path.cwd() / "ray-workshop", Path("/opt/app-root/src/ray-workshop")):
        root = candidate.resolve()
        if (root / _REPO_MARKER).is_file():
            return root

    raise FileNotFoundError(
        "Could not find ray-workshop (expected extras/scripts/scale_data.py). "
        "Clone the repo into your workbench or set RAY_WORKSHOP_REPO."
    )


def login(token: str, server: str) -> TokenAuthentication:
    """Authenticate to OpenShift (see RHOAI: Using the cluster server and token)."""
    skip_tls = os.environ.get("RAY_WORKSHOP_SKIP_TLS", "false").lower() in {
        "1",
        "true",
        "yes",
    }
    auth = TokenAuthentication(
        token=token.strip(),
        server=server.strip(),
        skip_tls=skip_tls,
    )
    auth.login()
    return auth


def show_local_queues(namespace: str = NAMESPACE):
    """List LocalQueues in the project (codeflare_sdk.list_local_queues)."""
    return list_local_queues(namespace)


def cpu_cluster_config(num_workers: int = 2) -> ManagedClusterConfig:
    """CPU Ray cluster for ephemeral RayJob labs (ManagedClusterConfig)."""
    return ManagedClusterConfig(
        num_workers=num_workers,
        head_cpu_requests=1,
        head_cpu_limits=2,
        head_memory_requests=2,
        head_memory_limits=4,
        worker_cpu_requests=1,
        worker_cpu_limits=2,
        worker_memory_requests=2,
        worker_memory_limits=4,
    )


def runtime_env_for_script(
    *,
    pip: list[str] | None = None,
    env_vars: dict[str, str] | None = None,
) -> dict:
    """Package the cloned repo as the Ray job working directory."""
    root = str(repo_root())
    return {
        "working_dir": root,
        "pip": pip or [],
        "env_vars": env_vars or {},
    }


def submit_rayjob(job: RayJob) -> RayJob:
    """Submit a RayJob and return the job object for status/logs."""
    job.submit()
    print(f"Submitted RayJob: {job.job_name}")
    return job


def wait_for_rayjob(job: RayJob, timeout_sec: int = 900) -> str:
    """Poll job.status() via CodeFlare SDK until terminal state."""
    terminal = {"SUCCEEDED", "FAILED", "STOPPED", "STOPPING"}
    deadline = time.time() + timeout_sec
    last = ""
    while time.time() < deadline:
        last = str(job.status())
        print(f"RayJob {job.job_name}: {last}")
        if last.upper() in terminal or last in terminal:
            return last
        time.sleep(15)
    raise TimeoutError(f"Timed out waiting for RayJob {job.job_name} (last status: {last})")


def print_job_logs(job: RayJob, tail: int = 80) -> None:
    """Print RayJob driver logs (CodeFlare SDK)."""
    logs = job.logs()
    if not logs:
        print("(no logs yet)")
        return
    lines = logs.splitlines()
    for line in lines[-tail:]:
        print(line)
