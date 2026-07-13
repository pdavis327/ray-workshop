# 3. Distributed compute (CodeFlare)

<p align="center">
<a href="/docs/02-ray-data-cluster.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-observe-and-manage.md">Next</a>
</p>

### Objectives (~20 min)

- Submit a second RayJob for **Ray Core task parallelism**.
- Show that OpenShift AI handles general distributed Python — not only ML frameworks.

### Hands-on

1. Open `extras/notebooks/03-distributed-compute-rayjob.ipynb`.
2. Run all cells.

### What happens

`distributed_stats.py` loads the bundled Iris CSV, splits rows into partitions, and runs `@ray.remote` tasks across workers. Results are printed as JSON in the job logs.

### Checklist

- [ ] RayJob `ray-workshop-distributed-stats` completes.
- [ ] Logs show partition summaries and `Aggregated row count: 30`.

### Demo talking point

No TensorFlow or PyTorch required — Ray on OpenShift AI is for **any** parallel Python: ETL, simulation, hyperparameter search, feature engineering.

<p align="center">
<a href="/docs/02-ray-data-cluster.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-observe-and-manage.md">Next</a>
</p>
