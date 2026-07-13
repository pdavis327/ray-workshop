"""Shared helpers for CodeFlare workshop notebooks."""

from __future__ import annotations

import os
import time
from pathlib import Path

from codeflare_sdk import ManagedClusterConfig, TokenAuthentication
from codeflare_sdk import RayJob  # noqa: F401 — re-exported for notebooks

NAMESPACE = os.environ.get("RAY_WORKSHOP_NAMESPACE", "ray-workshop")
LOCAL_QUEUE = os.environ.get("RAY_WORKSHOP_LOCAL_QUEUE", "ray-workshop-queue")


def repo_root() -> Path:
    """Workbench clone path; override with RAY_WORKSHOP_REPO."""
    return Path(os.environ.get("RAY_WORKSHOP_REPO", Path.cwd())).resolve()


def login(token: str, server: str) -> TokenAuthentication:
    """Authenticate to OpenShift for CodeFlare SDK."""
    auth = TokenAuthentication(token=token.strip(), server=server.strip(), skip_tls=True)
    auth.login()
    return auth


def cpu_cluster_config(num_workers: int = 2) -> ManagedClusterConfig:
    """Small CPU Ray cluster for workshop labs."""
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


def submit_rayjob(job: RayJob) -> str:
    """Submit and print the RayJob name."""
    name = job.submit()
    print(f"Submitted RayJob: {name}")
    return name


def wait_for_rayjob(name: str, namespace: str = NAMESPACE, timeout_sec: int = 900) -> None:
    """Poll RayJob status via the Kubernetes API (requires cluster access)."""
    from kubernetes import client, config

    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()

    api = client.CustomObjectsApi()
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        obj = api.get_namespaced_custom_object(
            group="ray.io",
            version="v1",
            namespace=namespace,
            plural="rayjobs",
            name=name,
        )
        status = obj.get("status", {})
        job_status = status.get("jobStatus", "unknown")
        print(f"RayJob {name}: jobStatus={job_status}")
        if job_status in {"SUCCEEDED", "FAILED", "STOPPED"}:
            return
        time.sleep(15)
    raise TimeoutError(f"Timed out waiting for RayJob {name}")
