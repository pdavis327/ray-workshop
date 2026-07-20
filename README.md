# ray-workshop

Hands-on workshop for [Ray-based distributed workloads on Red Hat OpenShift AI 3.4](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads), using the CodeFlare SDK with KubeRay and Kueue.

**Audience:** data scientists and platform engineers  
**Duration:** ~85 minutes (Topics 0–4)  
**Namespace:** `ray-workshop`

**Start here → [Topic 0 — Setup](/docs/00-setup.md)**

## Lab sequence

| Step | Topic | Notebook / focus |
|------|--------|------------------|
| [0 – Setup](/docs/00-setup.md) | Workbench, clone repo | — |
| [1 – Ray Data](/docs/01-ray-data-cluster.md) | Shared cluster + `job_client` | `01-ray-data-job-client.ipynb` |
| [2 – Distributed compute](/docs/02-distributed-compute.md) | Ray Core `@ray.remote` | `02-distributed-compute-job-client.ipynb` |
| [3 – Ray Train + MLflow](/docs/03-ray-train.md) | GPU Train, metrics, registry | `03-ray-train-job-client.ipynb` |
| [4 – Troubleshooting](/docs/04-troubleshooting.md) | Common failures | — |

Topics 1–3 reuse one GPU RayCluster named `ray-workshop` (`ensure_workshop_cluster`). Tear down at the end of Topic 3.

## What you will use

| Piece | Role in this workshop |
|-------|------------------------|
| CodeFlare SDK | Auth, LocalQueues, create/attach RayCluster, `job_client` |
| KubeRay | Runs the `RayCluster` (head + 2×GPU workers) |
| Kueue | Admits the cluster via LocalQueue → ClusterQueue |
| MLflow | Topic 3 tracking + model registry (dashboard URI + **user** token) |

Stack background and CRDs: [architecture](/docs/architecture.md). Official overview: [distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/overview-of-distributed-workloads_distributed-workloads).

## Learning outcomes

- Authenticate with Console token (`AuthConfig`), discover queues, inspect clusters
- Submit Ray Data / Ray Core / Ray Train jobs via `cluster.job_client`
- Log Train metrics, a checkpoint artifact, and a registered model to OpenShift AI MLflow

Serving is out of scope — continue with [kserve-workshop](https://github.com/redhat-ai-americas/kserve-workshop).

## Facilitator

Live delivery: [facilitator cheat sheet](/docs/facilitator-cheat-sheet.md). Platform prep: [prerequisites](/docs/prerequisites.md).

```sh
CLUSTER_QUEUE=default bash scripts/setup.sh -s 1
bash scripts/sanity_check.sh
```

Requires GPU quota on the ClusterQueue (2× `nvidia.com/gpu`). YAML under `configs/facilitator/` is optional smoke testing only — not the participant path.

## Official references

1. [Running Ray workloads from Jupyter](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads)
2. [Tame Ray workloads on OpenShift AI](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue) (workspace + job client workflow)
3. [Supported configurations](https://access.redhat.com/articles/6856871)
