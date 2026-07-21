# Architecture

Based on [Overview of distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/overview-of-distributed-workloads_distributed-workloads) and the [KubeRay + Kueue developer article](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue).

## Workshop path: workspace cluster + job client

```
Data scientist (Jupyter workbench)
        ↓ CodeFlare SDK (AuthConfig + set_api_client)
    Cluster + ClusterConfiguration → RayCluster CR (name: ray-workshop)
        ↓
    LocalQueue (namespace) → ClusterQueue (cluster)   [Kueue]
        ↓ admitted
    KubeRay operator → Ray head + 2×GPU worker pods
        ↓
    cluster.job_client.submit_job(...)  →  Ray Jobs API on the head
        ↓
    Topics 1–2 leave cluster up; Topic 3 calls cluster.down()
```

| CRD | Scope | Purpose |
|-----|-------|---------|
| LocalQueue | Namespace | Team/project queue; CodeFlare sets `local_queue=` |
| ClusterQueue | Cluster | Quota pool (needs GPU quota for this workshop) |
| RayCluster | Namespace | Shared workspace cluster for Topics 1–3 |
| RayJob | Namespace | Facilitator YAML / production path — not the primary lab SDK path |

1. Participant clones repo into workbench storage.
2. `Cluster.apply()` creates or updates shared `RayCluster` `ray-workshop`; Kueue admits via `ray-workshop-queue`.
3. KubeRay creates head + workers (reused across Topics 1–3).
4. `job_client.submit_job()` runs topic scripts with `runtime_env.working_dir`.
5. Participant tears down with `cluster.down()` at the end of Topic 3.

Jobs appear in the **Ray Dashboard → Jobs** tab. They are not always Kubernetes `RayJob` CRs.

## Other CodeFlare workflows (not this lab)

| Workflow | SDK | Notes |
|----------|-----|-------|
| Workspace + job client | `Cluster` / `job_client` | **This workshop** |
| Job via RayJob CR on existing cluster | `RayJob(cluster_name=...)` | Skipped (TLS issues on some lab APIs) |
| Ephemeral automated job | `RayJob` + `ManagedClusterConfig` | Facilitator YAML / production reference |

## Facilitator YAML

`configs/facilitator/` — optional `oc apply` smoke tests without a workbench. Participants use CodeFlare SDK only.
