# 2. Ephemeral RayJob — Ray Data

<p align="center">
<a href="/docs/01-workbench-smoke-test.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/03-distributed-compute.md">Next</a>
</p>

### Objectives (~25 min)

- Submit an ephemeral RayJob with `RayJob` + `ManagedClusterConfig` (official workflow 3).
- Run the same `scale_data.py` script on a KubeRay-managed cluster.

Reference: [Ephemeral cluster: self-service automated jobs](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue#the_ephemeral_cluster__self_service__automated_jobs) and [Running Ray workloads from Jupyter](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads).

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/02-ray-data-rayjob.ipynb`.
2. When you reach the auth cell, get credentials from the **OpenShift Console** (not from `oc whoami` inside the workbench):

   - Console → your username → **Copy login command** → Display token
   - Paste the `server` and `token` into the notebook

   For lab clusters with self-signed certificates, the notebook sets `skip_tls=True` on `TokenAuthentication` (the article default is `False`).

   Per [Using the cluster server and token to authenticate](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/preparing-the-distributed-training-environment_distributed-workloads#using-the-cluster-server-and-token-to-authenticate_preparing-the-distributed-training-environment).

3. Run all cells. The notebook calls CodeFlare `list_local_queues("ray-workshop")` after login.

### Pattern (CodeFlare SDK)

```python
from codeflare_sdk import RayJob, ManagedClusterConfig, TokenAuthentication

auth = TokenAuthentication(token="...", server="...", skip_tls=True)
auth.login()

job = RayJob(
    job_name="ray-workshop-scale-data",
    entrypoint="python extras/scripts/scale_data.py",
    cluster_config=ManagedClusterConfig(num_workers=2, ...),
    namespace="ray-workshop",
    local_queue="ray-workshop-queue",
    runtime_env={
        "working_dir": "<repo>",
        "pip": ["pyarrow", "pandas"],
        "env_vars": {"INPUT_PATH": "extras/data/iris.csv", ...},
    },
)
job.submit()
job.status()
job.logs()
```

KubeRay creates the cluster, runs the job, and deletes the cluster when finished.

### Demo talking points

- Data scientist defines resources inline — no Kubernetes YAML.
- Kueue admits the job when `ClusterQueue` quota allows.
- Same script as Topic 1; only execution location changes.

### Checklist

- [ ] `job.submit()` succeeds.
- [ ] `job.status()` reaches a terminal success state.
- [ ] `job.logs()` contains `Done. Wrote N parquet file(s)`.

<p align="center">
<a href="/docs/01-workbench-smoke-test.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/03-distributed-compute.md">Next</a>
</p>
