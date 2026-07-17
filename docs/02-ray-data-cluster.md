# 2. Workspace cluster + job client — Ray Data

<p align="center">
<a href="/docs/01-workbench-smoke-test.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/03-distributed-compute.md">Next</a>
</p>

### Objectives (~25 min)

- Create a `RayCluster` with CodeFlare `Cluster` + `ClusterConfiguration`.
- Submit `scale_data.py` with `cluster.job_client` (same script as Topic 1).

Reference: [Running Ray workloads from Jupyter](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads) and [workspace / job-client workflows](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue).

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/02-ray-data-job-client.ipynb`.
2. When you reach the auth cell, get credentials from the **OpenShift Console** (not from `oc whoami` inside the workbench):

   - Console → your username → **Copy login command** → Display token
   - Paste the `server` and `token` into the notebook

   Lab clusters with self-signed certificates use `AuthConfig(..., verify_ssl=False)`.

3. Run all cells through job submit and logs. Call `cluster.down()` when finished (or leave the cluster up for Topic 4).

### Pattern (CodeFlare SDK)

```python
from kube_authkit import AuthConfig, get_k8s_client
from codeflare_sdk import set_api_client, Cluster, ClusterConfiguration

set_api_client(get_k8s_client(config=AuthConfig(
    method="openshift",
    k8s_api_host="...",
    token="...",
    verify_ssl=False,
)))

cluster = Cluster(ClusterConfiguration(
    name="ray-workshop-data",
    namespace="ray-workshop",
    local_queue="ray-workshop-queue",
    num_workers=2,
    ...
))
cluster.apply()
cluster.wait_ready()

client = cluster.job_client
submission_id = client.submit_job(
    entrypoint="python extras/scripts/scale_data.py",
    runtime_env={"working_dir": "<repo>", "pip": ["pyarrow", "pandas"], ...},
)
client.get_job_status(submission_id)
client.get_job_logs(submission_id)

cluster.down()
```

### Demo talking points

- Data scientist defines resources in Python — no Kubernetes YAML.
- Kueue admits the **RayCluster** when `ClusterQueue` quota allows.
- `job_client` submits to the Ray head (Jobs API); watch status in the notebook or Ray Dashboard → Jobs.
- Same script as Topic 1; only execution location changes.
- Always `cluster.down()` when done so quota is released.

### Checklist

- [ ] `cluster.wait_ready()` succeeds.
- [ ] Job reaches `SUCCEEDED`.
- [ ] Logs contain `Done. Wrote N parquet file(s)`.
- [ ] `cluster.down()` completed (unless intentionally left up for Topic 4).

<p align="center">
<a href="/docs/01-workbench-smoke-test.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/03-distributed-compute.md">Next</a>
</p>
