# 3. Ephemeral RayJob — distributed compute

<p align="center">
<a href="/docs/02-ray-data-cluster.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-observe-and-manage.md">Next</a>
</p>

### Objectives (~20 min)

- Submit a second ephemeral RayJob for Ray Core task parallelism (`@ray.remote`).
- Monitor with `job.status()` and `job.logs()`.

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/03-distributed-compute-rayjob.ipynb`.
2. When you reach the auth cell, paste the same OpenShift Console **server** and **token** as [Topic 2](/docs/02-ray-data-cluster.md#hands-on).
3. Run all cells.

### What happens

`distributed_stats.py` partitions the Iris CSV and runs `@ray.remote` tasks across workers. Results appear in job logs.

### Checklist

- [ ] RayJob completes successfully.
- [ ] Logs show partition summaries and `Aggregated row count: 30`.

### Demo talking point

Ray on OpenShift AI supports general distributed Python — not only ML frameworks.

<p align="center">
<a href="/docs/02-ray-data-cluster.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-observe-and-manage.md">Next</a>
</p>
