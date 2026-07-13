# Architecture

```mermaid
flowchart TB
  subgraph OCP["OpenShift AI project: ray-workshop"]
    WB[Workbench notebook]
    CF[CodeFlare SDK]
    LQ[LocalQueue / Kueue]
    RJ[RayJob CR]
    subgraph KubeRay["KubeRay operator"]
      HEAD[Ray head pod]
      W1[Ray worker pod]
      W2[Ray worker pod]
    end
  end

  WB --> CF
  CF -->|RayJob + ManagedClusterConfig| RJ
  LQ -->|admits| RJ
  RJ --> HEAD
  RJ --> W1
  RJ --> W2
  CF -->|runtime_env working_dir| HEAD
  CF -->|runtime_env working_dir| W1
  CF -->|runtime_env working_dir| W2
```

## Data flow (Ray Data lab)

1. Participant clones `ray-workshop` into workbench storage.
2. CodeFlare `RayJob` packages the repo via `runtime_env.working_dir`.
3. `scale_data.py` reads `extras/data/iris.csv`, adds `petal_area`, writes Parquet to `/tmp/ray-workshop-output/iris/`.
4. KubeRay tears down the ephemeral cluster when the job finishes.

## Facilitator YAML path (optional)

Under `configs/facilitator/`, manifests use ConfigMaps and PVCs for smoke tests without a workbench. Participants do **not** use this path.
