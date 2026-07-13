# 1. Workbench smoke test (local Ray Data)

<p align="center">
<a href="/docs/00-setup.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/02-ray-data-cluster.md">Next</a>
</p>

### Objectives (~10 min)

- Validate the lab script in the workbench before submitting ephemeral RayJobs.
- If local works but cluster fails, suspect platform configuration — not your Python.

Topic 2 uses the [ephemeral RayJob pattern](https://developers.redhat.com/articles/2025/12/03/tame-ray-workloads-openshift-ai-kuberay-and-kueue#the_ephemeral_cluster__self_service__automated_jobs) (`RayJob` + `ManagedClusterConfig`).

### Where this runs

- OpenShift AI workbench (JupyterLab), project `ray-workshop`
- "Local" = Ray inside the workbench pod, not a KubeRay cluster
- No OpenShift API token required for this topic

### Hands-on

After [cloning the repo in Topic 0](/docs/00-setup.md#4-clone-the-repo), switch from the terminal to the **file browser** (folder icon in the left sidebar).

1. Navigate to `ray-workshop` → `extras` → `notebooks`.
2. Open `01-local-smoke.ipynb`.
3. Run all cells.

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
