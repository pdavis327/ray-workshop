# 1. Workbench smoke test (local Ray Data)

<p align="center">
<a href="/docs/00-setup.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/02-ray-data-cluster.md">Next</a>
</p>

### Objectives (~10 min)

- Run Ray Data **inside your OpenShift AI workbench** before submitting cluster jobs.
- Confirm the lab script and bundled dataset work in the same environment you will use for CodeFlare labs.

### Where this runs
- **OpenShift AI workbench** (JupyterLab in the browser)
- Project: **`ray-workshop`** 

**"Local"** in this topic means Ray runs **inside the workbench pod** on the cluster — not on a separate KubeRay cluster. Topic 2 uses the **same script** but Ray runs on **KubeRay worker pods** submitted via CodeFlare.

```
Topic 1:  Workbench → Ray starts locally in the workbench → scale_data.py
Topic 2:  Workbench → CodeFlare RayJob → KubeRay pods → scale_data.py
```

### Prerequisites

Complete [Topic 0 — Setup](/docs/00-setup.md) first:

- [ ] Workbench **Running** in project `ray-workshop`
- [ ] Repo cloned under `/opt/app-root/src/ray-workshop` (or your clone path)
- [ ] `pip install` completed (`ray`, `pyarrow`, `pandas`)

## 1. Open the workshop notebook

1. In JupyterLab, open the file browser.
2. Navigate to `ray-workshop/extras/notebooks/`.
3. Open **`01-local-smoke.ipynb`**.

Or read the steps below and use the workbench terminal instead.

## 2. Run the smoke test

**Option A — notebook (recommended)**

1. Run all cells in `01-local-smoke.ipynb`.
2. The notebook runs `extras/scripts/scale_data.py` with paths pointing at the bundled Iris CSV.

**Option B — workbench terminal**

```sh
cd /opt/app-root/src/ray-workshop
export INPUT_PATH=$PWD/extras/data/iris.csv
export OUTPUT_DIR=$PWD/tmp/iris-local
python extras/scripts/scale_data.py
ls tmp/iris-local/
```

## 3. What you should see

- Log lines showing Ray started a **local** Ray instance in the workbench.
- Printed **batch previews** including a new column `petal_area`.
- A final line similar to: `Done. Wrote N parquet file(s) to .../tmp/iris-local`.
- One or more `.parquet` files under `tmp/iris-local/`.

Warnings about `/dev/shm` or object store size are common in workbenches and can be ignored for this lab.

## Checklist

- [ ] Workbench is Running in `ray-workshop` (not your laptop).
- [ ] Batch previews print in the output.
- [ ] Parquet files appear under `tmp/iris-local/`.

### Takeaway

Topic 2 runs the **same script** on a Ray cluster via CodeFlare — the only change is **where Ray executes**. If this smoke test fails, fix paths or packages here before moving on. If this passes but the cluster RayJob fails, suspect platform configuration (Kueue, KubeRay, queues), not your Python code.

<p align="center">
<a href="/docs/00-setup.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/02-ray-data-cluster.md">Next</a>
</p>
