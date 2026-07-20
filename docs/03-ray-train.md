# 3. Workspace cluster + job client — Ray Train + MLflow

<p align="center">
<a href="/docs/02-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-troubleshooting.md">Next</a>
</p>

### Objectives (~25 min)

- Create a GPU `RayCluster` (2 workers × 1 GPU) with `workshop_cluster_configuration`.
- Submit distributed training with Ray Train `TorchTrainer` via `cluster.job_client`.
- Match `ScalingConfig(num_workers=2, use_gpu=True)` to the cluster GPU layout.
- Log params/metrics to **MLflow** and register the PyTorch model in the MLflow Model Registry.

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/03-ray-train-job-client.ipynb`.
2. Paste the same OpenShift Console **server** and **token** as [Topic 1](/docs/01-ray-data-cluster.md#hands-on).
3. Set `MLFLOW_TRACKING_URI` to your in-cluster MLflow service (see below).
4. Run all cells (create cluster → submit `train_fashion_mnist.py` → logs → `view_clusters()` → `cluster.down()`).
5. Open the MLflow UI → experiment `ray-workshop-fashion-mnist` → confirm metrics and registered model `ray-workshop-fashion-mnist`.

### MLflow URI (OpenShift AI)

From a terminal with cluster access:

```sh
oc get svc mlflow-server -n mlflow \
  -o go-template='{{.metadata.name}}.{{.metadata.namespace}}.svc.cluster.local:{{(index .spec.ports 0).port}}{{println}}'
```

Typical value: `http://mlflow-server.mlflow.svc.cluster.local:8080`.

The notebook passes `MLFLOW_TRACKING_AUTH=kubernetes-namespaced` for MLflow deployed on OpenShift AI (same pattern as other OAI demos). Ray workers must be able to reach that service from the `ray-workshop` project.

### What happens

`train_fashion_mnist.py` runs FashionMNIST on GPUs with Ray Train. The driver opens an MLflow run (params + tags). Rank 0 logs epoch `loss` and registers the model with `mlflow.pytorch.log_model`.

Workers need egress (or pre-cached data) for FashionMNIST, and network path to MLflow. Prefer a CUDA-capable Ray image from [Supported Configurations](https://access.redhat.com/articles/6856871); the notebook also installs `torch` / `torchvision` / `mlflow` via `runtime_env.pip` when needed.

Serving the registered model (KServe) is out of scope here — see the companion [kserve-workshop](https://github.com/redhat-ai-americas/kserve-workshop).

### Demo talking points

- Platform layer (`Cluster`) vs application layer (`TorchTrainer` / Ray Train) vs experiment tracking (MLflow).
- GPU requests belong on **workers**, not the head — do not set `nvidia.com/gpu: 0`.
- `ScalingConfig.num_workers` must not exceed available GPU Ray workers or the job stays PENDING.
- Only rank 0 writes MLflow metrics/model so you get one clean run, not duplicates.

### Checklist

- [ ] `cluster.wait_ready()` succeeds (2 GPU workers).
- [ ] Job reaches `SUCCEEDED`.
- [ ] Logs show epoch losses, `MLflow run_id=...`, and `Done. Ray Train FashionMNIST finished successfully.`
- [ ] MLflow UI shows experiment `ray-workshop-fashion-mnist` and registered model `ray-workshop-fashion-mnist`.
- [ ] `cluster.down()` completed.

<p align="center">
<a href="/docs/02-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-troubleshooting.md">Next</a>
</p>
