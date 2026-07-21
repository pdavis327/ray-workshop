# 3. Workspace cluster + job client — Ray Train + MLflow

<p align="center">
<a href="/docs/02-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/README.md">Next</a>
</p>

### Objectives (~25 min)

- Attach or create the shared GPU `RayCluster` (`ray-workshop` via `Cluster.apply()`).
- Submit distributed training with Ray Train `TorchTrainer` via `cluster.job_client`.
- Match `ScalingConfig(num_workers=2, use_gpu=True)` to the cluster GPU layout.
- Log params/metrics to **MLflow**, save a `checkpoint.pt` artifact, log confusion counts, and register the PyTorch model.
- Tear the cluster down when finished.

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/03-ray-train-job-client.ipynb`.
2. Paste the same OpenShift Console **server** and **token** as [Topic 1](/docs/01-ray-data-cluster.md#hands-on).
3. Confirm `MLFLOW_TRACKING_URI` matches your cluster’s MLflow UI URL (see below) and that `MLFLOW_TRACKING_TOKEN` uses that same user token.
4. Run all cells (create/reuse cluster → submit → logs → `view_clusters()` → `cluster.down()`).
5. Open the MLflow UI → workspace/project `ray-workshop` → experiment `ray-workshop-fashion-mnist`.

### What Ray is doing

1. **Platform:** Same shared `ray-workshop` RayCluster + `job_client` as Topics 1–2. `runtime_env.pip` installs `torch` / `torchvision` / `mlflow` into the job env on those pods. See [architecture](/docs/architecture.md).
2. **Library (this topic): Ray Train** inside [`extras/scripts/train_fashion_mnist.py`](/extras/scripts/train_fashion_mnist.py):
   - `TorchTrainer` + `ScalingConfig(num_workers=2, use_gpu=True)` — one Train worker per GPU Ray worker
   - `prepare_model` / `prepare_data_loader` — distributed data-parallel training loop
   - Post-epoch eval metrics; final `checkpoint.pt` + confusion counts
3. **MLflow (not a Ray library):** params/metrics/artifacts and `mlflow.pytorch.log_model` → Model Registry. Tracking uses the dashboard URI + your **user** token.

**Unlike Topics 1–2**, this job uses the GPUs and the Train API (not Ray Data or bare `@ray.remote`). Checkpoint = raw weights; registered model = promotion artifact. Serving (KServe) is out of scope — see [kserve-workshop](https://github.com/redhat-ai-americas/kserve-workshop).

### MLflow URI and auth (OpenShift AI 3.4 managed)

Official pattern: [Install and authenticate the MLflow SDK](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_mlflow/installing-and-authenticating-mlflow-sdk_mlflow).

**Tracking URI** = dashboard MLflow URL (includes `/mlflow`):

```sh
oc get mlflow mlflow -n redhat-ods-applications -o jsonpath='{.status.url}{"\n"}'
```

Example: `https://<rhoai-dashboard-host>/mlflow`

**Auth from a Ray job:** pass `MLFLOW_TRACKING_TOKEN` = your OpenShift **user** token and `MLFLOW_WORKSPACE` = `ray-workshop`.

Do **not** rely on `MLFLOW_TRACKING_AUTH=kubernetes-namespaced` inside Ray workers. OpenShift AI’s gateway rejects Kubernetes service-account tokens for MLflow (known issue RHOAIENG-44516). The workshop passes the same Console token already used for CodeFlare.

Also set `MLFLOW_TRACKING_INSECURE_TLS=true` on lab clusters with self-signed certs. SDK: `mlflow[kubernetes]>=3.11`.

### What happens (MLflow details)

After Train finishes, the driver/rank-0 path logs `train_*` / `test_*` metrics, per-class counts, artifacts `checkpoint.pt` and `confusion_matrix.csv`, and registers the model with `mlflow.pytorch.log_model`.

**Checkpoint vs registered model:** `checkpoint.pt` is raw weights for resume/debug; the registered MLflow model is the promotion artifact.

### Demo talking points

- Platform (`Cluster`) vs Train (`TorchTrainer`) vs tracking (MLflow).
- MLflow workspace maps 1:1 to the OpenShift project (`ray-workshop`).
- User token for MLflow API; SA tokens do not work through the RHOAI MLflow gateway.
- One shared RayCluster across Topics 1–3; tear down here.

### Checklist

- [ ] `cluster.wait_ready()` succeeds (2 GPU workers).
- [ ] Job reaches `SUCCEEDED`.
- [ ] Logs show epoch `train_*` / `test_*`, `final test_accuracy`, `MLflow run_id=...`, and `Done. Ray Train FashionMNIST finished successfully.`
- [ ] MLflow UI (workspace `ray-workshop`) shows charts, `checkpoint.pt`, confusion artifact, and registered model.
- [ ] `cluster.down()` completed.

<p align="center">
<a href="/docs/02-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/README.md">Next</a>
</p>
