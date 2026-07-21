# 1. Workspace cluster + job client — Ray Data

<p align="center">
<a href="/docs/00-setup.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/02-distributed-compute.md">Next</a>
</p>

### Objectives (~25 min)

- Discover LocalQueues with `list_local_queues()`.
- Create or reuse the shared `ray-workshop` RayCluster (`Cluster` + `apply` + `wait_ready`).
- Submit `scale_data.py` with `cluster.job_client`.
- Inspect with `view_clusters()` (Ray Dashboard → Jobs).
- Leave the cluster up for Topics 2–3.

Reference: [Running Ray workloads from Jupyter](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads) and [workspace / job-client workflows](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue).

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/01-ray-data-job-client.ipynb`.
2. When you reach the auth cell, get credentials from the **OpenShift Console** (not from `oc whoami` inside the workbench):

   - Console → your username → **Copy login command** → Display token
   - Paste the `server` and `token` into the notebook

   Lab clusters with self-signed certificates use `AuthConfig(..., verify_ssl=False)`.

3. Run cells: auth → `list_local_queues()` → create/reuse cluster → submit job → `view_clusters()`. **Skip tear-down** unless you are stopping for the day (Topic 3 tears down by default).

### Pattern (CodeFlare SDK)

```python
from kube_authkit import AuthConfig, get_k8s_client
from codeflare_sdk import (
    set_api_client, list_local_queues, view_clusters,
    Cluster, ClusterConfiguration,
)

set_api_client(get_k8s_client(config=AuthConfig(
    method="openshift",
    k8s_api_host="...",
    token="...",
    verify_ssl=False,
)))

list_local_queues("ray-workshop")

cluster = Cluster(ClusterConfiguration(
    name="ray-workshop",
    namespace="ray-workshop",
    local_queue="ray-workshop-queue",
    num_workers=2,
    # … CPU/memory + worker nvidia.com/gpu: 1 (see notebook)
))
cluster.apply()   # creates if missing, updates if present
cluster.wait_ready()

client = cluster.job_client
submission_id = client.submit_job(
    entrypoint="python extras/scripts/scale_data.py",
    runtime_env={"working_dir": "<repo>", "pip": ["pyarrow", "pandas"], ...},
)
client.get_job_status(submission_id)
client.get_job_logs(submission_id)

view_clusters("ray-workshop")
# Leave up for Topics 2–3; Topic 3 calls cluster.down()
```

### Demo talking points

- Data scientist defines resources in Python — no Kubernetes YAML.
- Default cluster shape: **2 workers × 1 GPU** (same `ClusterConfiguration` in Topics 1–3).
- Topics 1–3 share one cluster named `ray-workshop` to save GPU wait time.
- Kueue admits the **RayCluster** when `ClusterQueue` quota allows (including GPU quota).
- `job_client` submits to the Ray head (Jobs API); watch status in the notebook or Ray Dashboard → Jobs.

### Checklist

- [ ] `list_local_queues()` shows `ray-workshop-queue`.
- [ ] `cluster.wait_ready()` succeeds.
- [ ] Job reaches `SUCCEEDED`.
- [ ] Logs contain `Done. Wrote N parquet file(s)`.
- [ ] `view_clusters()` shows `ray-workshop`.
- [ ] Cluster left up for Topics 2–3 (unless intentionally torn down).

<p align="center">
<a href="/docs/00-setup.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/02-distributed-compute.md">Next</a>
</p>
