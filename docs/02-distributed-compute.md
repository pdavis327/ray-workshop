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

### What Ray is doing

1. **Platform:** Same as Topic 1 — shared `ray-workshop` cluster + `job_client` (no new pods per job). See [architecture](/docs/architecture.md).
2. **Library (this topic): Ray Core** inside [`extras/scripts/distributed_stats.py`](/extras/scripts/distributed_stats.py):
   - Split Iris rows into partitions
   - `@ray.remote` `summarize_partition(...)` — one task per partition on workers
   - `ray.get(...)` — collect summaries and aggregate counts

**Unlike Topic 1** (Ray Data dataset pipeline) you write explicit remote functions. **Unlike Topic 3** there is no Train/DDP or MLflow — just general distributed Python. GPUs on the shared cluster are unused here on purpose (same cluster shape for Topics 1–3).

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
