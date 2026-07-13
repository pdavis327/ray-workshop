# ray-workshop

Hands-on workshop for [Ray-based distributed workloads on Red Hat OpenShift AI 3.4](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads), using the CodeFlare SDK with KubeRay and Kueue.

Audience: Data scientists and platform engineers evaluating OpenShift AI distributed workloads.

Duration: About 80 minutes for Topics 0–5.

If you are starting the workshop, open [Topic 0 — Setup](/docs/00-setup.md).

Namespace: `ray-workshop`

## Official references (prioritized)

1. [Overview of distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/overview-of-distributed-workloads_distributed-workloads) — components and infrastructure
2. [Running Ray-based distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads) — CodeFlare SDK from Jupyter
3. [Tame Ray workloads on OpenShift AI (Red Hat Developer)](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue) — three CodeFlare workflows

## Background: What are we working with?

This workshop runs on the [OpenShift AI distributed workloads stack](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/overview-of-distributed-workloads_distributed-workloads). Four technologies do most of the work:

| Technology | What it is |
|------------|------------|
| Ray | Open source framework for scaling Python workloads across multiple machines. Turn laptop code into distributed code with minimal changes. |
| KubeRay | Kubernetes operator that runs and manages Ray on OpenShift. Creates head and worker pods from custom resources. |
| Kueue | Kubernetes-native job queuing. Traffic controller for cluster resources — fair sharing, priorities, and quotas. |
| CodeFlare SDK | Python SDK for data scientists. Submit Ray workloads from a Jupyter workbench without writing Kubernetes YAML or using `kubectl`. |

OpenShift AI ties these together: enable the `ray` and `kueue` components on the DataScienceCluster, use a workbench image that includes CodeFlare (for example Standard Data Science), and let cert-manager handle TLS for Ray clusters (mTLS enabled by default).

### KubeRay custom resources

KubeRay exposes Ray as Kubernetes CRDs. You rarely author these YAML files in this workshop — CodeFlare creates them — but they are what runs under the hood:

| CRD | Purpose |
|-----|---------|
| RayCluster | A Ray cluster: one head node plus worker nodes. Traditionally defined with complex YAML manifests. |
| RayJob | Manages the lifecycle of a Ray workload. Can spin up a temporary RayCluster, run your code, and tear down when finished — or submit against an existing RayCluster. |

### Kueue custom resources

Kueue admits workloads before pods are scheduled. This workshop uses LocalQueue and ClusterQueue directly; the others matter for platform design:

| CRD | Purpose |
|-----|---------|
| LocalQueue | Namespaced entry point where teams submit jobs. Aggregates a project's workloads and routes them to a ClusterQueue for admission. |
| ClusterQueue | Cluster-wide pool that enforces usage limits and quotas. Governs admission and fair sharing for workloads from multiple LocalQueues. |
| Cohort | Groups ClusterQueues so they can share unused quota. Busier queues borrow capacity from idle ones. |
| ResourceFlavor | Defines hardware variations available to the cluster (for example different GPU or CPU node types). |
| WorkloadPriorityClass | Job importance for scheduling order; critical workloads can preempt less important ones. |

In practice: participants reference a LocalQueue in the CodeFlare SDK; facilitators create LocalQueues and link them to a ClusterQueue.

## Three CodeFlare workflows

From the [Red Hat Developer article](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue#the_ephemeral_cluster__self_service__automated_jobs):

| Workflow | SDK pattern | This workshop |
|----------|-------------|---------------|
| Long-running workspace | `Cluster` + `ClusterConfiguration` | Not covered (see official `copy_demo_nbs()` demos) |
| Quick iteration on workspace | `RayJob` with `cluster_name=` | Not covered |
| Ephemeral automated job | `RayJob` + `ManagedClusterConfig` | Topics 2–3 (primary path) |

This workshop teaches the ephemeral cluster pattern: define cluster resources inline, submit once, KubeRay creates head + workers, job runs, cluster is removed when finished.

```
Workbench (CodeFlare SDK)
        ↓ RayJob + ManagedClusterConfig
    LocalQueue → ClusterQueue (Kueue admits)
        ↓
    KubeRay operator → Ray head + worker pods
        ↓
    Job completes → cluster torn down
```

## Learning outcomes

Participants should be able to:

- Describe the OpenShift AI distributed workloads stack (CodeFlare, KubeRay, Kueue).
- Authenticate with `TokenAuthentication` and discover LocalQueues with `list_local_queues()`.
- Submit an ephemeral `RayJob` with `ManagedClusterConfig` and monitor with `job.status()` / `job.logs()`.
- Observe RayJobs and queues with `view_clusters()` and the OpenShift AI console.

## Lab sequence (~80 min)

| Step | Topic | Time |
|------|--------|------|
| [0 – Setup](/docs/00-setup.md) | Workbench, auth, clone repo | ~10 min |
| [1 – Workbench smoke test](/docs/01-workbench-smoke-test.md) | `01-local-smoke.ipynb` | ~10 min |
| [2 – Ephemeral RayJob (Ray Data)](/docs/02-ray-data-cluster.md) | `02-ray-data-rayjob.ipynb` | ~25 min |
| [3 – Ephemeral RayJob (compute)](/docs/03-distributed-compute.md) | `03-distributed-compute-rayjob.ipynb` | ~20 min |
| [4 – Observe](/docs/04-observe-and-manage.md) | `04-observe-and-manage.ipynb` | ~10 min |
| [5 – Troubleshooting](/docs/05-troubleshooting.md) | Common issues | ~5 min |

## Facilitator automation

Prepare the project only. Participants create their own workbenches in Topic 0.

```sh
CLUSTER_QUEUE=default bash scripts/setup.sh -s 1
bash scripts/sanity_check.sh
```

See [Prerequisites](/docs/prerequisites.md) for Kueue dashboard enablement and hardware profiles.

YAML under `configs/facilitator/` is facilitator-only smoke testing.

## Companion workshop

Process and train with ray-workshop; serve models with [kserve-workshop](https://github.com/redhat-ai-americas/kserve-workshop).
