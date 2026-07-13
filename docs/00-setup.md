# 0. Prerequisites and setup

<p align="center">
<a href="/README.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/01-workbench-smoke-test.md">Next</a>
</p>

> All participant labs run from an OpenShift AI workbench (JupyterLab). You do not need `oc apply` or YAML.

Official procedure: [Running Ray-based distributed workloads from Jupyter notebooks](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads#running-distributed-data-science-workloads-from-jupyter-notebooks_running-ray-based-distributed-workloads).

## Who does what

| Task | Facilitator | Participant |
|------|-------------|-------------|
| Install distributed workloads components (`ray`, `kueue`) | yes | — |
| Enable Kueue in dashboard + hardware profiles | yes | — |
| Create `ray-workshop` project + LocalQueue | yes | — |
| Create workbench | — | yes |
| Clone repo + run notebooks | — | yes |

## Facilitator checklist

See [Prerequisites](/docs/prerequisites.md).

- [ ] `ray` and `kueue` enabled on DataScienceCluster
- [ ] `disableKueue: false` in OdhDashboardConfig
- [ ] Hardware profile with Local queue strategy (queue name exists in `ray-workshop`)
- [ ] `CLUSTER_QUEUE=default bash scripts/setup.sh -s 1`
- [ ] `bash scripts/sanity_check.sh` passes

## Participant checklist (~10 min)

- [ ] Log in to OpenShift AI
- [ ] Open project `ray-workshop` under A.I. projects
- [ ] Create workbench (steps below)
- [ ] Clone this repo inside the workbench
- [ ] Record OpenShift API token and server URL

## 1. Open the workshop project

1. Log in to the OpenShift AI dashboard.
2. Go to Projects → A.I. projects → Ray Workshop (`ray-workshop`).

## 2. Create your workbench

Per [Creating a workbench for distributed training](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/preparing-the-distributed-training-environment_distributed-workloads#creating-a-workbench-for-distributed-training_preparing-the-distributed-training-environment):

1. Workbenches tab → Create workbench.
2. Name: e.g. `ray-lab`.
3. Image: Standard Data Science (or any image with CodeFlare SDK per Supported Configurations).
4. Hardware profile: select a profile that uses Local queue allocation (required in Kueue-managed projects). If none appear, ask your facilitator — see [Prerequisites](/docs/prerequisites.md).
5. Create and wait until Running.

## 3. Open JupyterLab

Click the workbench name when Running.

## 4. Clone the repo

Terminal in JupyterLab:

```sh
cd /opt/app-root/src
git clone https://github.com/redhat-ai-americas/ray-workshop.git
cd ray-workshop
```

If CodeFlare is not in your image:

```sh
pip install codeflare-sdk pyarrow pandas "ray[default]>=2.52"
```

Optional — explore official SDK demo notebooks:

```python
from codeflare_sdk import copy_demo_nbs
copy_demo_nbs()
```

## 5. Authenticate (Topics 2–4)

Per [Using the cluster server and token to authenticate](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/preparing-the-distributed-training-environment_distributed-workloads#using-the-cluster-server-and-token-to-authenticate_preparing-the-distributed-training-environment):

```sh
oc whoami --show-server
oc whoami --show-token
```

Paste into notebook auth cells. Official default is `skip_tls=False`; for self-signed clusters set `export RAY_WORKSHOP_SKIP_TLS=true` before running notebooks.

## 6. Discover your LocalQueue

In a notebook (after auth):

```python
from codeflare_sdk import list_local_queues
list_local_queues("ray-workshop")
```

Workshop notebooks default to `ray-workshop-queue`. Override with `export RAY_WORKSHOP_LOCAL_QUEUE=default` if your admin configured a different queue.

## Notebook order

| Notebook | Topic |
|----------|--------|
| `01-local-smoke.ipynb` | 1 |
| `02-ray-data-rayjob.ipynb` | 2 — ephemeral RayJob |
| `03-distributed-compute-rayjob.ipynb` | 3 — ephemeral RayJob |
| `04-observe-and-manage.ipynb` | 4 — `view_clusters()` |

<p align="center">
<a href="/README.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/01-workbench-smoke-test.md">Next</a>
</p>
