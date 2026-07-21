# 0. Prerequisites and setup

<p align="center">
<a href="/README.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/01-ray-data-cluster.md">Next</a>
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

See [Prerequisites](/docs/prerequisites.md) and the [facilitator cheat sheet](/docs/facilitator-cheat-sheet.md).

- [ ] `ray` and `kueue` enabled on DataScienceCluster
- [ ] `disableKueue: false` in OdhDashboardConfig
- [ ] `CLUSTER_QUEUE=default bash scripts/setup.sh -s 1` (creates LocalQueues + `cpu-local-queue` HardwareProfile)
- [ ] `bash scripts/sanity_check.sh` passes

## Participant checklist (~10 min)

- [ ] Log in to OpenShift AI
- [ ] Open project `ray-workshop` under A.I. projects
- [ ] Create workbench (steps below)
- [ ] Clone this repo (step 4)

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
| **Terminal** (File → New → Terminal) | Clone the repo, install packages |
| **Notebooks** (file browser → `extras/notebooks/`) | All workshop labs |

Step 4 uses the terminal. After that, continue to [Topic 1 — Ray Data on cluster](/docs/01-ray-data-cluster.md).

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

Continue to [Topic 1 — Ray Data on cluster](/docs/01-ray-data-cluster.md).

## Notebook order

Workshop labs live under `extras/notebooks/` (not `demo-notebooks/`):

| Notebook | Topic | Ray library |
|----------|--------|-------------|
| `01-ray-data-job-client.ipynb` | 1 — cluster + job client (+ `view_clusters`) | **Ray Data** |
| `02-distributed-compute-job-client.ipynb` | 2 — cluster + job client | **Ray Core** (`@ray.remote`) |
| `03-ray-train-job-client.ipynb` | 3 — GPU Train + MLflow | **Ray Train** (+ MLflow tracking) |

Same RayCluster / `job_client` platform in all three; different libraries inside each script. See [How the labs differ](/README.md#how-the-labs-differ).

Topics 1–3 prompt for OpenShift API credentials in the notebook when you need them.

> Optional only: `copy_demo_nbs()` copies **official CodeFlare SDK demos** into `demo-notebooks/`. Those are **not** this workshop — labs are `extras/notebooks/01–03` above.

<p align="center">
<a href="/README.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/01-ray-data-cluster.md">Next</a>
</p>
