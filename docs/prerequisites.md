# Prerequisites

Aligned with [OpenShift AI 3.4 — Running Ray-based distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads).

## Cluster (facilitator)

Install [distributed workloads components](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/installing_and_uninstalling_openshift_ai_self-managed/installing-the-distributed-workloads-components_install):

| DSC component | Setting | Purpose |
|---------------|---------|---------|
| `ray` | `Managed` | KubeRay operator, RayJob/RayCluster CRDs |
| `kueue` | `Unmanaged` | Integrate with Red Hat build of Kueue Operator |
| cert-manager | (cluster) | mTLS for Ray clusters |

Verify:

```sh
oc get dscinitialization,datasciencecluster -n redhat-ods-applications
oc api-resources | grep -E 'rayjob|raycluster|localqueue'
oc get pods -n redhat-ods-applications | grep kuberay
oc get pods -n openshift-kueue-operator
```

Worker capacity: at least **2 GPUs** plus head CPU/memory for the workshop RayCluster shape (2 workers × 1 GPU).

## OpenShift AI dashboard (facilitator)

Kueue-managed projects require:

1. `OdhDashboardConfig.spec.dashboardConfig.disableKueue: false` — [Enabling Kueue in the dashboard](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/managing_openshift_ai/managing-workloads-with-kueue)
2. A Kueue-enabled hardware profile with **Local queue** strategy (no node selectors). `setup.sh -s 1` applies `cpu-local-queue` in `redhat-ods-applications`, pointing at LocalQueue `default` by default.

The built-in default hardware profile often uses node selectors and will not appear in Kueue-managed projects like `ray-workshop`. Use `cpu-local-queue` instead.

Without both Kueue dashboard enablement and an eligible profile, participants may see no hardware profiles when creating a workbench.

## Participant workbench

Per RHOAI docs, use a workbench image that includes the CodeFlare SDK — for example the Standard Data Science notebook. See [Supported Configurations](https://access.redhat.com/articles/6856871) for your OpenShift AI version.

| Requirement | Notes |
|-------------|--------|
| OpenShift AI workbench | JupyterLab; project admin on `ray-workshop` |
| CodeFlare SDK | Pre-installed in Standard Data Science image, or `pip install codeflare-sdk` |
| OpenShift API token + server | [Using the cluster server and token to authenticate](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/preparing-the-distributed-training-environment_distributed-workloads#using-the-cluster-server-and-token-to-authenticate_preparing-the-distributed-training-environment) |
| LocalQueue in project | Facilitator `setup.sh -s 1` or dashboard-created project |

Optional: `copy_demo_nbs()` copies official CodeFlare SDK demos into `demo-notebooks/` — **not** the workshop path (`extras/notebooks/01–03`).

## Facilitator setup

```sh
CLUSTER_QUEUE=default bash scripts/setup.sh -s 1
bash scripts/sanity_check.sh
```

Creates namespace `ray-workshop`, LocalQueues (`default`, `ray-workshop-queue`), and HardwareProfile `cpu-local-queue` (CPU, Local queue → `default`).

Override the profile's LocalQueue reference:

```sh
HARDWARE_PROFILE_LOCAL_QUEUE=ray-workshop-queue CLUSTER_QUEUE=default bash scripts/setup.sh -s 1
```

## GPU Ray workloads

**Required for this workshop.** Labs use an inline `ClusterConfiguration` — 2 workers with `worker_extended_resource_requests={"nvidia.com/gpu": 1}` each. Facilitators must align three layers. Official references: [Managing distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/managing_openshift_ai/managing-distributed-workloads_managing-rhoai), [hardware profiles](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_accelerators/working-with-hardware-profiles_accelerators).

### How the pieces connect

```
ResourceFlavor (node pool label)
        ↓ referenced by
ClusterQueue (GPU quota under that flavor)
        ↓ fed by
LocalQueue (per-project inbox)
        ↓ referenced by
HardwareProfile type: Queue (workbench)  OR  CodeFlare RayJob local_queue=
```

### 1. ResourceFlavor

Kueue uses ResourceFlavor to name a hardware pool. Check what exists:

```sh
oc get resourceflavors
oc get resourceflavor nvidia-gpu-flavor -o yaml
```

If `spec` is empty (`spec: {}`), the flavor is a placeholder. Add node matching so Kueue knows which nodes count toward GPU quota — labels must match your GPU nodes (adjust for your cluster):

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: nvidia-gpu-flavor
spec:
  nodeLabels:
    nvidia.com/gpu.present: "true"
    # or: gpu-type: largegpu
```

Verify node labels on GPU workers match before applying.

### 2. ClusterQueue — add GPU quota

The auto-created `default` ClusterQueue often quotas only CPU and memory under `default-flavor`. Workshop RayClusters need `nvidia.com/gpu` in a resource group that references `nvidia-gpu-flavor` (at least quota **2** for one lab cluster).

Inspect current quota:

```sh
oc get clusterqueue default -o yaml
```

Extend or create a ClusterQueue per [RHOAI distributed workloads admin guide](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/managing_openshift_ai/managing-distributed-workloads_managing-rhoai). Conceptually, add a resource group like:

```yaml
resourceGroups:
  - coveredResources:
      - nvidia.com/gpu
    flavors:
      - name: nvidia-gpu-flavor
        resources:
          - name: nvidia.com/gpu
            nominalQuota: "4"   # example: 4 GPUs cluster-wide
```

CPU and GPU quotas can live in the same ClusterQueue or separate ClusterQueues linked to different LocalQueues.

### 3. HardwareProfile for Kueue-managed workbenches

In Kueue-managed projects, workbench profiles must use **`scheduling.type: Queue`** — not node selectors. GPU profiles used for KServe (`type: Node` with `gpu-type` selectors) will not appear in `ray-workshop`.

Create a GPU profile the same way as `cpu-local-queue`: Local queue strategy, LocalQueue name that exists in the project (e.g. `default`), plus GPU identifiers in `spec.identifiers`. Apply to `redhat-ods-applications`.

### 4. CodeFlare — request GPUs on workers

In `ClusterConfiguration` (workshop path) or `ManagedClusterConfig` (ephemeral RayJob), request accelerators on workers (from the [developer article](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue)):

```python
ClusterConfiguration(
    # ...
    worker_extended_resource_requests={"nvidia.com/gpu": 1},
)
```

Or with ManagedClusterConfig:

```python
ManagedClusterConfig(
    num_workers=2,
    worker_accelerators={"nvidia.com/gpu": 1},
    # ... cpu/memory requests ...
)
```

Omit GPU fields on the **head**. Do not set `nvidia.com/gpu: 0` (can break admission). Workshop default is workers-only GPUs in each Topic 1–3 notebook `ClusterConfiguration`.

Use a CUDA-capable Ray image per [Supported Configurations](https://access.redhat.com/articles/6856871).

### KServe vs Kueue GPU paths

| Use case | Scheduling | Example on this cluster |
|----------|------------|-------------------------|
| Model serving (KServe) | HardwareProfile `type: Node` + node selectors | `nvidia-l40s`, `nvidia-l4-small` (GitOps) |
| Ray workbench / RayJob in Kueue project | HardwareProfile `type: Queue` + LocalQueue | `cpu-local-queue` (workshop); create `gpu-local-queue` for GPU extension |

Do not assume a node-selector GPU profile works for Ray workbenches in `ray-workshop`.

## Disconnect / air-gap

- Mirror default Ray training images from [Supported Configurations](https://access.redhat.com/articles/6856871) if workers cannot reach registries.
- Bundled `extras/data/iris.csv` avoids external data dependencies.
- `runtime_env.pip` needs PyPI or pre-baked Ray image dependencies.
