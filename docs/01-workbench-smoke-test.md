# 1. Workbench smoke test

<p align="center">
<a href="/docs/00-setup.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/02-ray-data-cluster.md">Next</a>
</p>

Topic 1 runs **`scale_data.py` in the workbench pod** — the same script Topic 2 submits via **`cluster.job_client`** on a KubeRay cluster.

### Why this topic

1. **Validate the environment** — repo cloned, paths correct, Ray/pandas/pyarrow available — before OpenShift API auth, LocalQueues, and RayClusters.
2. **Separate failures** — if this notebook succeeds but Topic 2 fails, suspect **platform configuration** (token, queue, quota, RayCluster), not the lab Python.

**Local** means Ray runs **inside the workbench**, not on KubeRay workers. Topic 2 runs the same logic remotely via `Cluster` + `job_client`.

## What actually runs (not distributed)

Topic 1 does **not** create a Kubernetes RayCluster. The notebook (or terminal) simply runs the Python script:

```python
python extras/scripts/scale_data.py
```

Inside that script, Ray Data auto-starts a **local, single-node** Ray runtime in the workbench pod.

| | Topic 1 (here) | Topic 2+ |
|---|---|---|
| How | Run script in workbench | `Cluster` + `job_client` via CodeFlare |
| Ray | Local single-node in pod | KubeRay head + workers |
| Distributed? | No | Yes |

Open `extras/notebooks/01-local-smoke.ipynb` and run all cells.

- **Recommended** for first-time runs.
- **Optional** if you skip straight to `02-ray-data-job-client.ipynb`.

If local Ray fails due to workbench memory limits, you may still proceed to Topic 2 — the main workshop path is the KubeRay cluster, not local Ray in the workbench.

### Checklist

- Validate the lab script in the workbench before submitting to the cluster.

Topic 2 uses the workspace cluster + job client pattern (`Cluster` + `cluster.job_client`).

<p align="center">
<a href="/docs/00-setup.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/02-ray-data-cluster.md">Next</a>
</p>
