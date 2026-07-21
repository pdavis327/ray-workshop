# Facilitator cheat sheet

Quick reference for live delivery. Participants follow Topics [0](/docs/00-setup.md)–[4](/docs/04-troubleshooting.md). Full failures: [Topic 4](/docs/04-troubleshooting.md).

## Timing tip

Topics **1–3 share one RayCluster** named `ray-workshop` (same `Cluster` + `ClusterConfiguration` in each notebook). Leave it up after Topics 1–2; tear down at the end of Topic 3. Saves GPU admission wait between labs.

## Expected job log lines

| Topic | Notebook / script | Look for |
|-------|-------------------|----------|
| 1 | `scale_data.py` | `Done. Wrote N parquet file(s)` |
| 2 | `distributed_stats.py` | Partition JSON + `Aggregated row count: 30` |
| 3 | `train_fashion_mnist.py` | `epoch: … train_loss … train_accuracy … test_*`, `final test_accuracy`, `MLflow run_id=…`, `Done. Ray Train FashionMNIST finished successfully.` |

Jobs appear under **Ray Dashboard → Jobs** (from `view_clusters()`), not necessarily as Kubernetes `RayJob` CRs.

## MLflow UI checks (Topic 3)

Workspace/project: **`ray-workshop`**

Experiment: **`ray-workshop-fashion-mnist`**

| Check | Expect |
|-------|--------|
| Metrics | `train_loss`, `train_accuracy`, `test_loss`, `test_accuracy` (per epoch); `final_test_*`; `class_accuracy_0`…`9` |
| Artifacts | `checkpoint.pt` (raw weights), `confusion_matrix.csv`, `model/` |
| Registry | Registered model **`ray-workshop-fashion-mnist`** |

Talking point: **checkpoint** = resume/debug weights; **registered model** = promotion artifact. Serving → [kserve-workshop](https://github.com/redhat-ai-americas/kserve-workshop).

### Auth reminder

```sh
oc get mlflow mlflow -n redhat-ods-applications -o jsonpath='{.status.url}{"\n"}'
```

Pass Console **user** token as `MLFLOW_TRACKING_TOKEN` (same as CodeFlare). Do **not** use Ray SA + `kubernetes-namespaced` (RHOAIENG-44516). Lab TLS: `MLFLOW_TRACKING_INSECURE_TLS=true`.

## Top failures (fast triage)

| Symptom | Fix |
|---------|-----|
| 401 / HTML login to MLflow | Fresh Console **user** token; URI must end with `/mlflow` |
| RayCluster Suspended / no pods | Wrong LocalQueue; missing **GPU quota** on ClusterQueue |
| Head `OOMKilled` / BackOff | Raise head memory (workshop defaults ≥8Gi limits); `cluster.down()` and recreate |
| Train job PENDING | `NUM_WORKERS` must be 2 (match GPU workers) |
| Token / `system:anonymous` | Re-paste Console token after kernel restart |

Reset:

```sh
oc delete raycluster --all -n ray-workshop
```

## Facilitator prep

```sh
CLUSTER_QUEUE=default bash scripts/setup.sh -s 1
bash scripts/sanity_check.sh
```

See [Prerequisites](/docs/prerequisites.md) and [Topic 0](/docs/00-setup.md).
