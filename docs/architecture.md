# Architecture

Based on [Overview of distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/overview-of-distributed-workloads_distributed-workloads) and the [KubeRay + Kueue developer article](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue).

## Infrastructure

```
Data scientist (Jupyter workbench)
        ↓ CodeFlare SDK (AuthConfig + set_api_client)
    Cluster + ClusterConfiguration  →  RayCluster CR
        ↓
    LocalQueue (namespace) → ClusterQueue (cluster)   [Kueue]
        ↓ admitted
    KubeRay operator → Ray head + worker pods
        ↓
    cluster.job_client.submit_job(...)  →  Ray Jobs API on the head
        ↓
    Job finishes → participant calls cluster.down()
```

| CRD | Scope | Purpose |
|-----|-------|---------|
| LocalQueue | Namespace | Team/project queue; CodeFlare sets `local_queue=` |
| ClusterQueue | Cluster | Quota pool; admits workloads |
| ResourceFlavor | Cluster | Node pool type for quota (e.g. `default-flavor`) |
| RayCluster | Namespace | Workspace cluster for Topics 1–3 |
| RayJob | Namespace | KubeRay job CR (facilitator YAML / production path; not the primary lab SDK path) |

## Workshop path: workspace cluster + job client

This workshop uses a **long-lived workspace `RayCluster`** plus **`cluster.job_client`** (Ray Jobs API):

1. Participant clones repo into workbench storage.
2. `Cluster.apply()` creates a `RayCluster` CR; Kueue admits via `ray-workshop-queue`.
3. KubeRay creates head + workers.
4. `job_client.submit_job()` runs `scale_data.py` / `distributed_stats.py` with `runtime_env.working_dir`.
5. Participant tears down with `cluster.down()`.

Jobs appear in the **Ray Dashboard → Jobs** tab. They are not always Kubernetes `RayJob` CRs.

## Other workflows (official)

| Workflow | SDK | Use case |
|----------|-----|----------|
| Workspace cluster + job client | `Cluster`, `job_client` | Interactive / lab iteration (**this workshop**) |
| Job on workspace via RayJob CR | `RayJob(cluster_name=...)` | Platform-visible jobs on an existing cluster |
| Ephemeral automated job | `RayJob` + `ManagedClusterConfig` | Batch / production (facilitator YAML; SDK path can hit TLS issues on self-signed lab APIs) |

## Facilitator YAML

`configs/facilitator/` — optional `oc apply` smoke tests without a workbench. Participants use CodeFlare SDK only.
