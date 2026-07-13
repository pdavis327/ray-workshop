# ray-workshop

Hands-on workshop for running Ray distributed workloads on **Red Hat OpenShift AI** with the **CodeFlare SDK**, **KubeRay**, and **Kueue**.

Audience: Data scientists and ML engineers evaluating or using OpenShift AI for distributed Python and data processing.

Duration: About **80 minutes** for Topics 0–5.

Format: Setup → local smoke test → **CodeFlare RayJob labs from a workbench** → observe on platform → troubleshooting.

If you are starting the workshop, open [the first set of instructions](/docs/00-setup.md).

Namespace: All labs use project **`ray-workshop`**.

## The stack

```
Data scientist (notebook)
        ↓ CodeFlare SDK
    RayJob CR  ←—— Kueue (quota / queue)
        ↓ KubeRay operator
   Ray head + workers (pods)
```

| Component | Customer-facing value |
|-----------|------------------------|
| **Ray** | Distributed Python — data, tasks, training |
| **CodeFlare SDK** | Submit jobs from notebook; no YAML required |
| **KubeRay** | Creates and destroys Ray clusters on OpenShift |
| **Kueue** | Fair scheduling, quotas, gang scheduling |
| **OpenShift AI** | Workbenches, DSC components, unified experience |

All labs run from an **OpenShift AI workbench** in project `ray-workshop` ([setup](/docs/00-setup.md)).

### RayJob lifecycle

1. Job submitted from notebook
2. Kueue admits when quota allows
3. KubeRay creates head + workers
4. Job runs; logs visible in console
5. Cluster **automatically deleted** when finished

## Learning outcomes

Participants should be able to:

- Explain how Ray, CodeFlare, KubeRay, Kueue, and OpenShift AI fit together.
- Run a local Ray Data smoke test **from an OpenShift AI workbench**.
- Submit **RayJobs** with the CodeFlare SDK (`RayJob` + `ManagedClusterConfig`).
- Monitor jobs from the notebook and OpenShift AI console.
- Describe how Kueue admits workloads and KubeRay manages cluster lifecycle.

## Lab sequence (~80 min)

| Step | Topic | Time |
|------|--------|------|
| [0 – Setup](/docs/00-setup.md) | Create workbench, clone repo, install packages | ~10 min |
| [1 – Workbench smoke test](/docs/01-workbench-smoke-test.md) | `01-local-smoke.ipynb` | ~10 min |
| [2 – Ray Data on cluster](/docs/02-ray-data-cluster.md) | `02-ray-data-rayjob.ipynb` | ~25 min |
| [3 – Distributed compute](/docs/03-distributed-compute.md) | `03-distributed-compute-rayjob.ipynb` | ~20 min |
| [4 – Observe & manage](/docs/04-observe-and-manage.md) | `04-observe-and-manage.ipynb` | ~10 min |
| [5 – Troubleshooting](/docs/05-troubleshooting.md) | Pitfalls and reset steps | ~5 min |

## Facilitator automation

Prepare the **project** only (namespace, AI project label, LocalQueue). **Participants create their own workbenches** in [Topic 0](/docs/00-setup.md).

```sh
bash scripts/setup.sh -s 0   # Web Terminal, banner, auto-clone
CLUSTER_QUEUE=default bash scripts/setup.sh -s 1
bash scripts/sanity_check.sh
```

Cluster admin: set `disableKueue: false` in `OdhDashboardConfig` so workbench creation works in Kueue-enabled projects.

YAML under `configs/facilitator/` is for facilitator smoke tests only — participants use notebooks.

## Primary documentation

- [Architecture](/docs/architecture.md)
- [Prerequisites](/docs/prerequisites.md)
- [Troubleshooting](/docs/troubleshooting.md)
- [OpenShift AI — Working with distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html-single/working_with_distributed_workloads/)
- [CodeFlare RayJob SDK](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue)

## Companion workshop

Process and train with **ray-workshop**; serve models with [kserve-workshop](https://github.com/redhat-ai-americas/kserve-workshop).
