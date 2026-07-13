# Prerequisites

## Cluster

| Requirement | Notes |
|-------------|--------|
| OpenShift 4.x | Tested pattern matches OpenShift AI Self-Managed 3.4 |
| OpenShift AI | DataScienceCluster installed |
| KubeRay (`ray` component) | Provides `RayCluster`, `RayJob` CRDs |
| Kueue (`kueue` component) | Quota-aware job admission |
| Worker CPU capacity | ~6–8 CPUs for concurrent labs (2-worker RayJobs) |

## Participant workbench

All hands-on labs (Topics 1–4) run from an **OpenShift AI workbench** in project `ray-workshop`. See [Topic 0 — Setup](/docs/00-setup.md) for step-by-step workbench creation.

| Requirement | Notes |
|-------------|--------|
| OpenShift AI workbench | JupyterLab in the browser — primary lab environment |
| **CodeFlare SDK** | Included in some workbench images; or `pip install codeflare-sdk` in Topic 0 |
| **kubernetes** Python package | For `wait_for_rayjob()` in notebooks: `pip install kubernetes` |
| Ray + PyArrow + Pandas | `pip install "ray[default]>=2.52" pyarrow pandas` (Topic 0) |
| OpenShift API token | `oc whoami --show-token` and `--show-server` (Topics 2–4) |
| Project access on `ray-workshop` | Submit RayJobs via CodeFlare |

## Facilitator-only

| Requirement | Notes |
|-------------|--------|
| Cluster admin (step 0) | Web Terminal operator subscription |
| `CLUSTER_QUEUE` name | Kueue ClusterQueue bound to LocalQueue (default on many clusters: `default`) |
| `OdhDashboardConfig` | `disableKueue: false` so participants can create workbenches in the UI |
| Image pull | Workers pull `rayproject/ray:2.52.0` from the internet OR mirror to internal registry |
| `oc` CLI | For `setup.sh` and `sanity_check.sh` |

## Pre-flight commands

```sh
oc get dscinitialization,datasciencecluster -n redhat-ods-applications
oc api-resources | grep -E 'rayjob|raycluster|localqueue'
bash scripts/sanity_check.sh
```

## Disconnect / air-gap notes

- Mirror `rayproject/ray:2.52.0` if workers cannot reach Docker Hub.
- Bundled `extras/data/iris.csv` avoids external S3 dependencies.
- PyArrow/Pandas install at job runtime via CodeFlare `runtime_env.pip` — ensure cluster can reach PyPI or pre-bake into a custom Ray image.
