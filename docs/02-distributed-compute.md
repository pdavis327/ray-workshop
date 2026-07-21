# 2. Workspace cluster + job client — distributed compute

<p align="center">
<a href="/docs/01-ray-data-cluster.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/03-ray-train.md">Next</a>
</p>

### Objectives (~20 min)

- Create or reuse the shared `ray-workshop` cluster (same `ClusterConfiguration` as Topic 1).
- Submit a second job for Ray Core task parallelism (`@ray.remote`) via `job_client`.
- Monitor with `client.get_job_status()` and `client.get_job_logs()`.
- Leave the cluster up for Topic 3.

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/02-distributed-compute-job-client.ipynb`.
2. When you reach the auth cell, paste the same OpenShift Console **server** and **token** as [Topic 1](/docs/01-ray-data-cluster.md#hands-on).
3. Run cells (create/reuse cluster → submit → logs). **Skip tear-down** unless you are stopping early (Topic 3 tears down by default).

### What happens

`distributed_stats.py` partitions the Iris CSV and runs `@ray.remote` tasks across workers. Results appear in job logs.

Uses the same **2×GPU** shared cluster as Topic 1 (GPUs unused by this script but keep the workshop cluster shape consistent).

### Checklist

- [ ] Job completes successfully.
- [ ] Logs show partition summaries and `Aggregated row count: 30`.
- [ ] Cluster left up for Topic 3.

### Demo talking point

Ray on OpenShift AI supports general distributed Python — not only ML frameworks.

<p align="center">
<a href="/docs/01-ray-data-cluster.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/03-ray-train.md">Next</a>
</p>
