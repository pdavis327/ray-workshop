# 3. Workspace cluster + job client — distributed compute

<p align="center">
<a href="/docs/02-ray-data-cluster.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-ray-train.md">Next</a>
</p>

### Objectives (~20 min)

- Submit a second job for Ray Core task parallelism (`@ray.remote`) via `job_client`.
- Monitor with `client.get_job_status()` and `client.get_job_logs()`.

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/03-distributed-compute-job-client.ipynb`.
2. When you reach the auth cell, paste the same OpenShift Console **server** and **token** as [Topic 2](/docs/02-ray-data-cluster.md#hands-on).
3. Run all cells (create cluster → submit → logs → `cluster.down()`).

### What happens

`distributed_stats.py` partitions the Iris CSV and runs `@ray.remote` tasks across workers. Results appear in job logs.

Uses the same **2×GPU** `workshop_cluster_configuration` as Topic 2 (GPUs unused by this script but keep the workshop cluster shape consistent).

### Checklist

- [ ] Job completes successfully.
- [ ] Logs show partition summaries and `Aggregated row count: 30`.
- [ ] Cluster torn down.

### Demo talking point

Ray on OpenShift AI supports general distributed Python — not only ML frameworks.

<p align="center">
<a href="/docs/02-ray-data-cluster.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-ray-train.md">Next</a>
</p>
