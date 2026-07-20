# 3. Workspace cluster + job client — Ray Train + MLflow

<p align="center">
<a href="/docs/02-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-troubleshooting.md">Next</a>
</p>

### Objectives (~25 min)

- Attach or create the shared GPU `RayCluster` (`ray-workshop` via `ensure_workshop_cluster`).
- Submit distributed training with Ray Train `TorchTrainer` via `cluster.job_client`.
- Match `ScalingConfig(num_workers=2, use_gpu=True)` to the cluster GPU layout.
- Log params/metrics to **MLflow**, save a `checkpoint.pt` artifact, log confusion counts, and register the PyTorch model.
- Tear the cluster down when finished.

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/03-ray-train-job-client.ipynb`.
2. Paste the same OpenShift Console **server** and **token** as [Topic 1](/docs/01-ray-data-cluster.md#hands-on).
3. Confirm `MLFLOW_TRACKING_URI` matches your cluster’s MLflow UI URL (see below) and that `MLFLOW_TRACKING_TOKEN` uses that same user token.
4. Run all cells (attach/create cluster → submit → logs → `view_clusters()` → `cluster.down()`).
5. Open the MLflow UI → workspace/project `ray-workshop` → experiment `ray-workshop-fashion-mnist`.

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

### What happens

`train_fashion_mnist.py` runs FashionMNIST on GPUs with Ray Train. The driver opens an MLflow run (params + tags). After each epoch, rank 0 runs `eval()` and logs `train_loss` / `train_accuracy` / `test_loss` / `test_accuracy`. At the end it logs final test metrics, per-class counts (`class_correct_*` / `class_accuracy_*`), artifacts `checkpoint.pt` and `confusion_matrix.csv`, and registers the model with `mlflow.pytorch.log_model`.

**Checkpoint vs registered model:** `checkpoint.pt` is raw weights for resume/debug; the registered MLflow model is the promotion artifact.

Serving the registered model (KServe) is out of scope — see [kserve-workshop](https://github.com/redhat-ai-americas/kserve-workshop).

### Demo talking points

- Platform (`Cluster`) vs Train (`TorchTrainer`) vs tracking (MLflow).
- MLflow workspace maps 1:1 to the OpenShift project (`ray-workshop`).
- User token for MLflow API; SA tokens do not work through the RHOAI MLflow gateway.
- One shared RayCluster across Topics 1–3; tear down here.

### Checklist

- [ ] `ensure_workshop_cluster` / `wait_ready` succeeds (2 GPU workers).
- [ ] Job reaches `SUCCEEDED`.
- [ ] Logs show epoch `train_*` / `test_*`, `final test_accuracy`, `MLflow run_id=...`, and `Done. Ray Train FashionMNIST finished successfully.`
- [ ] MLflow UI (workspace `ray-workshop`) shows charts, `checkpoint.pt`, confusion artifact, and registered model.
- [ ] `cluster.down()` completed.

<p align="center">
<a href="/docs/02-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/04-troubleshooting.md">Next</a>
</p>
