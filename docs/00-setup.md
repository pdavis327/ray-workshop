# 0. Prerequisites and setup

<p align="center">
<a href="/README.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/01-workbench-smoke-test.md">Next</a>
</p>

> **All participant labs run from an OpenShift AI workbench** (JupyterLab in the browser). You do not need `oc apply`, YAML, or a local laptop install of Ray for the hands-on exercises.

## Who does what

| Task | Facilitator | Participant |
|------|-------------|-------------|
| Enable `ray` + Kueue on cluster | ✅ | — |
| Enable Kueue in OpenShift AI dashboard | ✅ | — |
| Create `ray-workshop` **project** (namespace + LocalQueue) | ✅ | — |
| Create **workbench** | — | ✅ (steps below) |
| Clone repo + run notebooks | — | ✅ |

**Facilitators prepare the project; participants create their own workbench.** No shared or pre-created workbench is provided.

## Official reference

- [Working with distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html-single/working_with_distributed_workloads/) (match doc version to your OpenShift AI release)
- [Creating a project workbench](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_on_projects/using-project-workbenches_projects)

## Facilitator checklist

- [ ] OpenShift AI with **`ray`** and **`kueue`** components enabled.
- [ ] Kueue enabled in dashboard: `OdhDashboardConfig.spec.dashboardConfig.disableKueue: false`.
- [ ] `CLUSTER_QUEUE=default bash scripts/setup.sh -s 1` (creates AI project + LocalQueue).
- [ ] `bash scripts/sanity_check.sh` passes.

Setup applies `opendatahub.io/dashboard=true` so **`ray-workshop` appears under A.I. projects** in the OpenShift AI UI.

## Participant checklist (~10 min)

- [ ] Log in to the **OpenShift AI dashboard**.
- [ ] Open project **`ray-workshop`** (under **A.I. projects**).
- [ ] **Create your workbench** (steps below).
- [ ] Clone this repo **inside the workbench**.
- [ ] Install Python packages in the workbench.
- [ ] Record OpenShift API **token** and **server URL** for Topics 2–4.

## 1. Open the workshop project

1. Log in to the **OpenShift AI** dashboard (from the OpenShift console application menu, or your organization's OpenShift AI URL).
2. Go to **Projects**.
3. Under **A.I. projects**, open **`Ray Workshop`** (`ray-workshop`).
4. If you do not see it, switch the filter to **All projects** or ask your facilitator to run setup step 1.

## 2. Create your workbench

You will use **one workbench** for Topics 1–4. **Each participant creates their own** — the facilitator does not create workbenches for you.

1. Open the **Workbenches** tab for `ray-workshop`.
2. Click **Create workbench**.
3. **Name:** e.g. `ray-lab` (use your name or initials if sharing a cluster).
4. **Image:** choose a Python workbench image that includes the **CodeFlare SDK** if your OpenShift AI version lists one (check *Supported Configurations* for your release).  
   If no CodeFlare image is available, choose **`Jupyter | Minimal | CPU | Python 3.12`** (or similar) — you will `pip install codeflare-sdk` in step 4 below.
5. **Hardware profile:** select **default-profile** (or your cluster's default CPU profile). This workbench only needs modest CPU/RAM for Topic 1 and for submitting jobs in Topics 2–4; Ray worker pods run separately on the cluster.
6. **Cluster storage:** accept the default size (workshop files and parquet output are small).
7. Click **Create workbench** and wait until the state is **Running**.

More detail: [Creating a project workbench](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_on_projects/using-project-workbenches_projects).

## 3. Open the workbench

1. When the workbench is **Running**, click its name.
2. Your browser opens **JupyterLab** (or the IDE your cluster provides) — this environment runs on the cluster, not on your laptop.

## 4. Clone the repo and install packages

Open a **terminal** in the workbench (JupyterLab: *File → New → Terminal*).

```sh
cd /opt/app-root/src
git clone https://github.com/redhat-ai-americas/ray-workshop.git
cd ray-workshop
pip install kubernetes pyarrow pandas "ray[default]>=2.52" codeflare-sdk
```

If `git clone` fails (no outbound HTTPS), ask your facilitator for a fork URL, upload a zip of the repo to the workbench, or use `oc cp` from a machine that has the files.

Verify the lab data is present:

```sh
ls extras/data/iris.csv extras/scripts/scale_data.py
```

## 5. Get your OpenShift token (for Topics 2–4)

CodeFlare notebooks need your cluster API URL and token. From the **workbench terminal** (if `oc` is available) or from your laptop:

```sh
oc whoami --show-server
oc whoami --show-token
```

Save both values — you will paste them into notebooks `02`–`04`.

If `oc` is not installed in the workbench, use the OpenShift web console: click your username → **Copy login command** → run the displayed `oc login` in a local terminal, then run the commands above.

## 6. Verify platform (optional)

Facilitators or participants with CLI access:

```sh
bash scripts/sanity_check.sh
```

## Notebook order

| Notebook | Topic |
|----------|--------|
| `01-local-smoke.ipynb` | 1 — run **in this workbench** |
| `02-ray-data-rayjob.ipynb` | 2 |
| `03-distributed-compute-rayjob.ipynb` | 3 |
| `04-observe-and-manage.ipynb` | 4 |

Open notebooks from the JupyterLab file browser under `ray-workshop/extras/notebooks/`.

## How to read these docs in the workbench

| Approach | How |
|----------|-----|
| JupyterLab | Open `docs/01-workbench-smoke-test.md` in the file browser |
| Terminal | `less docs/00-setup.md` (quit with `q`) |
| Browser | Read the same files on GitHub while using the workbench for commands |

<p align="center">
<a href="/README.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/01-workbench-smoke-test.md">Next</a>
</p>
