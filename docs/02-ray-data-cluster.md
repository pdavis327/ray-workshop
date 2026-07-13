# 2. Ray Data on the cluster (CodeFlare)

<p align="center">
<a href="/docs/01-workbench-smoke-test.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/03-distributed-compute.md">Next</a>
</p>

### Objectives (~25 min)

- Submit a **RayJob** from the workbench using the CodeFlare SDK.
- Run distributed Ray Data ETL on KubeRay-managed workers.

### Hands-on

1. Open `extras/notebooks/02-ray-data-rayjob.ipynb`.
2. Set `OPENSHIFT_SERVER` and `OPENSHIFT_TOKEN` in the auth cell.
3. Run all cells.

### What the notebook does

```python
from codeflare_sdk import RayJob, ManagedClusterConfig

job = RayJob(
    job_name="ray-workshop-scale-data",
    entrypoint="python extras/scripts/scale_data.py",
    cluster_config=ManagedClusterConfig(num_workers=2, ...),
    namespace="ray-workshop",
    local_queue="ray-workshop-queue",
    runtime_env={
        "working_dir": "<cloned-repo>",
        "pip": ["pyarrow", "pandas"],
        "env_vars": {"INPUT_PATH": "extras/data/iris.csv", ...},
    },
)
job.submit()
```

KubeRay creates the cluster, Ray packages your repo to workers, and the job tears down when finished.

### Demo talking points

- Data scientist never wrote Kubernetes YAML.
- **Kueue** admitted the job to the `ray-workshop-queue`.
- Same OpenShift AI project, enterprise quotas, audit trail in `oc get rayjob`.

### Checklist

- [ ] `job.submit()` succeeds.
- [ ] `wait_for_rayjob` reports `SUCCEEDED` (or RayJob shows complete in console).
- [ ] Head pod logs contain `Done. Wrote N parquet file(s)`.

### Under the hood (show briefly)

```sh
oc get rayjob ray-workshop-scale-data -n ray-workshop
```

<p align="center">
<a href="/docs/01-workbench-smoke-test.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/03-distributed-compute.md">Next</a>
</p>
