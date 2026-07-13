# 1. Workbench smoke test (local Ray Data)

<p align="center">
<a href="/docs/00-setup.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/02-ray-data-cluster.md">Next</a>
</p>

## Purpose

Topic 1 runs **`scale_data.py` in the workbench pod** — the same script Topic 2 submits as an ephemeral **RayJob** on a KubeRay cluster.

We do this to:

1. **Validate the environment** — repo cloned, paths correct, Ray/pandas/pyarrow available — before OpenShift API auth, LocalQueues, and RayJobs.
2. **Separate failures** — if this notebook succeeds but Topic 2 fails, suspect **platform configuration** (token, queue, quota, RayJob), not the lab Python.
3. **Introduce Ray Data on a tiny dataset** — read CSV, `map_batches`, write Parquet — without CodeFlare or cluster lifecycle in the same step.

**Local** means Ray runs **inside the workbench**, not on KubeRay workers. Topic 2 runs the same logic remotely via `RayJob` + `ManagedClusterConfig`.

## What actually runs (not distributed)

Topic 1 does **not** submit a Kubernetes **RayJob**. The notebook (or terminal) simply runs the Python script:

```sh
python extras/scripts/scale_data.py
```

Inside that script, **Ray Data** calls auto-start a **local, single-node** Ray runtime in the workbench pod. There is no KubeRay cluster, no worker pods, and no multi-node scheduling — on this tiny Iris dataset it is effectively one process in one pod.

| | Topic 1 (here) | Topic 2+ |
|---|---|---|
| How | Run script in workbench | Submit **RayJob** via CodeFlare |
| Ray | Local single-node in pod | KubeRay head + workers |
| Distributed? | No | Yes |

**Ray job** (generic Ray work) ≠ **RayJob** (KubeRay custom resource on OpenShift).

## Required?

- **Recommended** for first-time runs and facilitators validating a new cluster.
- **Optional** if you are comfortable skipping straight to [Topic 2](/docs/02-ray-data-cluster.md).

If local Ray fails due to workbench memory limits, you may still proceed to Topic 2 — the main workshop path is the RayJob on KubeRay, not local Ray in the workbench.

## What this does not prove

- Kueue admission or LocalQueue configuration
- CodeFlare authentication or `RayJob` submission
- Multi-node or production-scale Ray

Those are Topics 2–4.

### Objectives (~10 min)

- Validate the lab script in the workbench before submitting ephemeral RayJobs.
- If local works but cluster fails, suspect platform configuration — not your Python.

Topic 2 uses the [ephemeral RayJob pattern](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue#the_ephemeral_cluster__self_service__automated_jobs) (`RayJob` + `ManagedClusterConfig`).

### Where this runs

- OpenShift AI workbench (JupyterLab), project `ray-workshop`
- No OpenShift API token required

### Hands-on

After [cloning the repo in Topic 0](/docs/00-setup.md#4-clone-the-repo):

1. Navigate to `ray-workshop` → `extras` → `notebooks`.
2. Open `01-local-smoke.ipynb` (read the intro cell for purpose and when to skip).
3. Run all cells.

The notebook finds the repo by walking up from the notebook directory (JupyterLab sets `cwd` to `.../ray-workshop/extras/notebooks`). You do not need to `cd` anywhere first.

Or from the workbench terminal:

```sh
cd /opt/app-root/src/ray-workshop
export INPUT_PATH=$PWD/extras/data/iris.csv
export OUTPUT_DIR=$PWD/tmp/iris-local
python extras/scripts/scale_data.py
ls tmp/iris-local/
```

### Checklist

- [ ] Batch previews print (including `petal_area`).
- [ ] Parquet files under `tmp/iris-local/`.

<p align="center">
<a href="/docs/00-setup.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/02-ray-data-cluster.md">Next</a>
</p>
