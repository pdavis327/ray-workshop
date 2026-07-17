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
| ResourceFlavor | Kueue label for a node pool type (CPU vs GPU). ClusterQueues attach quota to flavors. See below. |
| WorkloadPriorityClass | Job importance for scheduling order; critical workloads can preempt less important ones. |

In practice: participants reference a LocalQueue in the CodeFlare SDK; facilitators create LocalQueues and link them to a ClusterQueue.

#### ResourceFlavor (platform)

A ResourceFlavor tells Kueue which **kind of nodes** a quota bucket applies to. ClusterQueues reference flavors when defining limits — for example `default-flavor` for CPU/memory on general nodes, or `nvidia-gpu-flavor` for GPU capacity.

OpenShift AI may auto-create flavors when Kueue is enabled. A flavor with empty `spec: {}` (like `nvidia-gpu-flavor` on many clusters) is a placeholder until a platform engineer adds `nodeLabels` and wires GPU quota into a ClusterQueue.

This workshop is **CPU-only** — Topics 0–5 use `cpu-local-queue` and `default-flavor`. GPU Ray clusters need additional facilitator setup; see [Prerequisites — Optional GPU extension](/docs/prerequisites.md#optional-gpu-ray-workloads).

## Why OpenShift AI instead of DIY upstream?

Ray, KubeRay, Kueue, and CodeFlare are all open source. You can install and connect them on any Kubernetes cluster yourself. Many teams start there — and many eventually hit the same wall: integration work, quota politics, and operational toil that has little to do with the models they are trying to build.

OpenShift AI is Red Hat's answer to that problem: a tested, supported platform that wires these projects together for enterprise use.

### DIY upstream: what you own

| Area | On your own |
|------|-------------|
| Operators | Install, upgrade, and version-match KubeRay, Kueue, and cert-manager; resolve controller conflicts |
| Security | Configure mTLS, network isolation, and Ray cluster hardening |
| Quotas | Wire Kueue admission webhooks to Ray CRDs, or run manual GPU approval queues |
| Developer experience | Data scientists write `RayCluster` / `RayJob` YAML or learn low-level cluster APIs |
| Observability | Piece together logs, metrics, and status across multiple operators |
| Air-gapped / regulated | Mirror images, document install paths, and test the full stack yourself |

This is workable for a skilled platform team. It is also ongoing work every time upstream ships a breaking change.

### What OpenShift AI and Red Hat builds add

Per the [distributed workloads overview](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/overview-of-distributed-workloads_distributed-workloads) and [managing workloads with Kueue](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/managing_openshift_ai/managing-workloads-with-kueue):

| Capability | Benefit |
|------------|---------|
| Integrated DSC components | Turn on `ray` and `kueue` on the DataScienceCluster; operators deploy and integrate with the OpenShift AI control plane |
| Red Hat build of Kueue Operator | Supported quota management, admission control, and prioritization for RayJobs, RayClusters, workbenches, and other workloads |
| Managed KubeRay | Ray clusters on OpenShift with controlled-network defaults and cert-manager-backed TLS |
| CodeFlare in workbench images | Submit from Jupyter in Python; SDK creates the Kubernetes objects — no YAML, no `kubectl` for data scientists |
| Dashboard and hardware profiles | Self-service workbench creation with Local queue allocation; view distributed workload status in one place |
| Documented operations | Install guides, [supported configurations](https://access.redhat.com/articles/6856871), disconnected paths, and [troubleshooting playbooks](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/troubleshooting-common-problems-with-distributed-workloads-for-users_distributed-workloads) |

You are not buying a different Ray. You are buying the integration, hardening, and operational model around it.

### From manual gatekeeper to self-service platform

The [Red Hat Developer article on KubeRay and Kueue](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue) frames the business case clearly:

Without Kueue, platform teams often become human schedulers — approving every GPU request, chasing forgotten clusters that idle overnight, and blocking data scientists on tickets. Utilization stays low; cost stays high.

With Kueue integrated into OpenShift AI, the model flips:

- Platform admins design quota policy once (ClusterQueues, priorities, cohorts) instead of approving every job.
- Data scientists self-serve through LocalQueues and the CodeFlare SDK — resources in seconds, not hours.
- Workspace clusters and jobs are admitted through LocalQueues — less ticket-queue scheduling.
- High-priority workloads can preempt lower-priority ones when quota is borrowed across teams.

That is why organizations invest in OpenShift AI rather than assembling the same stack by hand: less glue code and ticket-queue operations, more time for research and platform policy design — with a vendor-backed path when something breaks at 2 AM.

This workshop shows the data-scientist side of that story (CodeFlare from a workbench). Facilitator setup covers the platform side (LocalQueue, ClusterQueue, hardware profiles) that makes self-service possible.

## Three CodeFlare workflows

From the [Red Hat Developer article](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue#the_ephemeral_cluster__self_service__automated_jobs):

| Workflow | SDK pattern | This workshop |
|----------|-------------|---------------|
| Long-running workspace + job client | `Cluster` + `cluster.job_client` | Topics 2–3 (primary path) |
| Job via RayJob CR on existing cluster | `RayJob(cluster_name=...)` | Not covered (SDK TLS issues on some lab APIs) |
| Ephemeral automated job | `RayJob` + `ManagedClusterConfig` | Facilitator YAML / production reference |

This workshop teaches the **workspace cluster + job client** pattern: create a `RayCluster`, submit jobs to the Ray head with `job_client`, tear down with `cluster.down()`. That path is reliable from OpenShift AI workbenches (including self-signed lab API certs with `verify_ssl=False`).

```
Workbench (CodeFlare SDK)
        ↓ Cluster + ClusterConfiguration
    LocalQueue → ClusterQueue (Kueue admits)
        ↓
    KubeRay operator → Ray head + worker pods
        ↓
    cluster.job_client.submit_job(...)
        ↓
    cluster.down()
```

## Learning outcomes

Participants should be able to:

- Describe the OpenShift AI distributed workloads stack (CodeFlare, KubeRay, Kueue).
- Authenticate with `AuthConfig` / `set_api_client` and discover LocalQueues with `list_local_queues()`.
- Create a `RayCluster` and submit work with `cluster.job_client`, then tear down with `cluster.down()`.
- Observe clusters and jobs with `view_clusters()` and the Ray Dashboard.

## Lab sequence (~80 min)

| Step | Topic | Time |
|------|--------|------|
| [0 – Setup](/docs/00-setup.md) | Workbench, auth, clone repo | ~10 min |
| [1 – Workbench smoke test](/docs/01-workbench-smoke-test.md) | `01-local-smoke.ipynb` (recommended) | ~10 min |
| [2 – Ray Data on cluster](/docs/02-ray-data-cluster.md) | `02-ray-data-job-client.ipynb` | ~25 min |
| [3 – Distributed compute](/docs/03-distributed-compute.md) | `03-distributed-compute-job-client.ipynb` | ~20 min |
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
