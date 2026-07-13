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

Worker capacity: ~6–8 CPUs for a 2-worker RayJob lab.

## OpenShift AI dashboard (facilitator)

Kueue-managed projects require:

1. `OdhDashboardConfig.spec.dashboardConfig.disableKueue: false` — [Enabling Kueue in the dashboard](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/managing_openshift_ai/managing-workloads-with-kueue)
2. At least one enabled hardware profile with workload allocation strategy Local queue, pointing at a LocalQueue name that exists in participant projects (typically `default`)

Without both, participants may see no hardware profiles when creating a workbench in `ray-workshop`.

## Participant workbench

Per RHOAI docs, use a workbench image that includes the CodeFlare SDK — for example the Standard Data Science notebook. See [Supported Configurations](https://access.redhat.com/articles/6856871) for your OpenShift AI version.

| Requirement | Notes |
|-------------|--------|
| OpenShift AI workbench | JupyterLab; project admin on `ray-workshop` |
| CodeFlare SDK | Pre-installed in Standard Data Science image, or `pip install codeflare-sdk` |
| OpenShift API token + server | [Using the cluster server and token to authenticate](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/preparing-the-distributed-training-environment_distributed-workloads#using-the-cluster-server-and-token-to-authenticate_preparing-the-distributed-training-environment) |
| LocalQueue in project | Facilitator `setup.sh -s 1` or dashboard-created project |

Optional: explore official SDK demos with `from codeflare_sdk import copy_demo_nbs; copy_demo_nbs()` in the workbench.

## Facilitator setup

```sh
CLUSTER_QUEUE=default bash scripts/setup.sh -s 1
bash scripts/sanity_check.sh
```

Creates namespace `ray-workshop` with `opendatahub.io/dashboard=true`, Kueue label, and LocalQueue `ray-workshop-queue`.

## Disconnect / air-gap

- Mirror default Ray training images from [Supported Configurations](https://access.redhat.com/articles/6856871) if workers cannot reach registries.
- Bundled `extras/data/iris.csv` avoids external data dependencies.
- `runtime_env.pip` needs PyPI or pre-baked Ray image dependencies.
