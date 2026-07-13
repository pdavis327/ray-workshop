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
- [ ] `CLUSTER_QUEUE=default bash scripts/setup.sh -s 1` (creates LocalQueues + `cpu-local-queue` HardwareProfile)
- [ ] `bash scripts/sanity_check.sh` passes

## Participant checklist (~10 min)

- [ ] Log in to OpenShift AI
- [ ] Open project `ray-workshop` under A.I. projects
- [ ] Create workbench (steps below)
- [ ] Clone this repo (step 4)
- [ ] Save OpenShift API token and server URL for Topics 2–4 (step 5)
- [ ] Run [Topic 1](/docs/01-workbench-smoke-test.md) notebook

## 1. Open the workshop project

1. Log in to the OpenShift AI dashboard.
2. Go to Projects → A.I. projects → Ray Workshop (`ray-workshop`).

## 2. Create your workbench

Per [Creating a workbench for distributed training](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/preparing-the-distributed-training-environment_distributed-workloads#creating-a-workbench-for-distributed-training_preparing-the-distributed-training-environment):

1. Workbenches tab → Create workbench.
2. Name: e.g. `ray-lab`.
3. Image: Standard Data Science (or any image with CodeFlare SDK per Supported Configurations).
4. Hardware profile: select **CPU (local queue)** (`cpu-local-queue`). If none appear, ask your facilitator to run `bash scripts/setup.sh -s 1` — see [Prerequisites](/docs/prerequisites.md).
5. Create and wait until Running.

## 3. Open JupyterLab

Click the workbench name when Running.

You will use two areas in JupyterLab:

| Area | When to use it |
|------|----------------|
| **Terminal** (File → New → Terminal) | Clone the repo, install packages, copy your API token |
| **Notebooks** (file browser → `extras/notebooks/`) | All workshop labs, starting with Topic 1 |

Steps 4–5 use the terminal. After that, switch to notebooks for every topic.

## 4. Clone the repo

Open a terminal in JupyterLab (File → New → Terminal, or the terminal icon in the launcher).

```sh
cd /opt/app-root/src
git clone https://github.com/redhat-ai-americas/ray-workshop.git
cd ray-workshop
```

If CodeFlare is not in your image:

```sh
pip install codeflare-sdk pyarrow pandas "ray[default]>=2.52"
```

Optional — to explore official SDK demo notebooks, switch to a **new notebook** (File → New → Notebook), run this cell, then browse the copied files in the file browser:

```python
from codeflare_sdk import copy_demo_nbs
copy_demo_nbs()
```

## 5. Save credentials for Topics 2–4

Topic 1 does not need OpenShift API access. Before Topics 2–4, collect your token and server URL in the **same terminal**:

Per [Using the cluster server and token to authenticate](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/preparing-the-distributed-training-environment_distributed-workloads#using-the-cluster-server-and-token-to-authenticate_preparing-the-distributed-training-environment):

```sh
oc whoami --show-server
oc whoami --show-token
```

Keep the values handy. You will paste them into the auth cells in `02-ray-data-rayjob.ipynb`, `03-distributed-compute-rayjob.ipynb`, and `04-observe-and-manage.ipynb`.

For self-signed clusters, set this in the terminal before opening those notebooks:

```sh
export RAY_WORKSHOP_SKIP_TLS=true
```

## 6. Start Topic 1

Switch to the **file browser** (folder icon in the left sidebar). Open:

`ray-workshop` → `extras` → `notebooks` → `01-local-smoke.ipynb`

Run all cells. Continue with [Topic 1 — Workbench smoke test](/docs/01-workbench-smoke-test.md).

Topics 2–4 use the other notebooks in the same folder. The first CodeFlare notebook (`02-ray-data-rayjob.ipynb`) includes auth and `list_local_queues("ray-workshop")` — you do not need a separate setup step for that.

## Notebook order

| Notebook | Topic |
|----------|--------|
| `01-local-smoke.ipynb` | 1 |
| `02-ray-data-rayjob.ipynb` | 2 — ephemeral RayJob |
| `03-distributed-compute-rayjob.ipynb` | 3 — ephemeral RayJob |
| `04-observe-and-manage.ipynb` | 4 — `view_clusters()` |

Workshop notebooks default to LocalQueue `ray-workshop-queue`. Override with `export RAY_WORKSHOP_LOCAL_QUEUE=default` in the terminal if your facilitator configured a different queue.

<p align="center">
<a href="/README.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/01-workbench-smoke-test.md">Next</a>
</p>
