# Architecture

Based on [Overview of distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/overview-of-distributed-workloads_distributed-workloads) and the [KubeRay + Kueue developer article](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue).

## Infrastructure

```
Data scientist (Jupyter workbench)
        ↓ CodeFlare SDK (TokenAuthentication)
    RayJob CR  +  ManagedClusterConfig
        ↓
    LocalQueue (namespace) → ClusterQueue (cluster)   [Kueue]
        ↓ admitted
    KubeRay operator → Ray head + worker pods
        ↓
    Job completes → ephemeral cluster deleted
```

| CRD | Scope | Purpose |
|-----|-------|---------|
| LocalQueue | Namespace | Team/project queue; CodeFlare sets `local_queue=` |
| ClusterQueue | Cluster | Quota pool; admits workloads |
| RayJob | Namespace | Entrypoint + cluster spec or cluster reference |
| RayCluster | Namespace | Long-running workspace (not used in this workshop) |

## Workshop path: ephemeral RayJob

This workshop uses workflow 3 from the developer article — `RayJob` with embedded `ManagedClusterConfig`:

1. Participant clones repo into workbench storage.
2. `RayJob.submit()` creates a RayJob CR; Kueue admits via `ray-workshop-queue`.
3. KubeRay creates head + workers; Ray packages `runtime_env.working_dir`.
4. Script runs (`scale_data.py` or `distributed_stats.py`).
5. Cluster tears down when the job finishes (`shutdownAfterJobFinishes`).

## Other workflows (official, not in timed labs)

| Workflow | SDK | Use case |
|----------|-----|----------|
| Workspace cluster | `Cluster`, `ClusterConfiguration` | Interactive `ray.init(cluster_uri())` |
| Job on workspace | `RayJob(cluster_name=...)` | Fast iteration without new cluster startup |
| Ephemeral job | `RayJob` + `ManagedClusterConfig` | Batch / production runs (this workshop) |

Explore workspace and widget flows via `copy_demo_nbs()` — see RHOAI section 4.1.

## Facilitator YAML

`configs/facilitator/` — optional `oc apply` smoke tests without a workbench. Participants use CodeFlare SDK only.
