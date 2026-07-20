# 3. Workspace cluster + job client — Ray Train

<p align="center">
<a href="/docs/02-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-troubleshooting.md">Next</a>
</p>

### Objectives (~25 min)

- Create a GPU `RayCluster` (2 workers × 1 GPU) with `workshop_cluster_configuration`.
- Submit distributed training with Ray Train `TorchTrainer` via `cluster.job_client`.
- Match `ScalingConfig(num_workers=2, use_gpu=True)` to the cluster GPU layout.

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/03-ray-train-job-client.ipynb`.
2. Paste the same OpenShift Console **server** and **token** as [Topic 1](/docs/01-ray-data-cluster.md#hands-on).
3. Run all cells (create cluster → submit `train_fashion_mnist.py` → logs → `view_clusters()` → `cluster.down()`).

### What happens

`train_fashion_mnist.py` runs FashionMNIST on GPUs with Ray Train. The job process uses `TorchTrainer`; KubeRay workers each request one `nvidia.com/gpu`.

Workers need egress (or pre-cached data) to download FashionMNIST on first run. Prefer a CUDA-capable Ray image from [Supported Configurations](https://access.redhat.com/articles/6856871); the notebook also installs `torch` / `torchvision` via `runtime_env.pip` when needed.

### Demo talking points

- Platform layer (`Cluster`) vs application layer (`TorchTrainer` / Ray Train).
- GPU requests belong on **workers**, not the head — do not set `nvidia.com/gpu: 0`.
- `ScalingConfig.num_workers` must not exceed available GPU Ray workers or the job stays PENDING.

### Checklist

- [ ] `cluster.wait_ready()` succeeds (2 GPU workers).
- [ ] Job reaches `SUCCEEDED`.
- [ ] Logs show epoch losses and `Done. Ray Train FashionMNIST finished successfully.`
- [ ] `cluster.down()` completed.

<p align="center">
<a href="/docs/02-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-troubleshooting.md">Next</a>
</p>
