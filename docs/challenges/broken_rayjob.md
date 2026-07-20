# Challenge: diagnose a stuck RayCluster (facilitator / advanced)

> Optional stretch. The main workshop path is `Cluster` + `job_client`.

Optional exercise (~10 min) for facilitators or advanced participants.

## Scenario A — notebook (participant path)

In Topic 1, 2, or 3, deliberately set a wrong queue:

```python
LOCAL_QUEUE = "does-not-exist-queue"
```

1. `cluster.apply()` and observe the RayCluster stay suspended / never ready.
2. Inspect:

```sh
oc get workload -n ray-workshop
oc describe workload <name> -n ray-workshop
oc describe localqueue -n ray-workshop
```

3. Fix `LOCAL_QUEUE` back to `ray-workshop-queue`, `cluster.down()` any stuck cluster, and retry.

## Scenario B — YAML (facilitator only)

`configs/challenges/broken-rayjob.yaml` uses a bad Kueue queue annotation and undersized head memory.

1. Apply: `oc apply -f configs/challenges/broken-rayjob.yaml`
2. Observe failure mode (`oc describe rayjob`, events, pod status).
3. Fix queue → `ray-workshop-queue`, head memory → at least `2Gi`, re-apply.

## Solution hints

- Kueue events mention unknown or inactive queue names.
- OOMKilled head pod → increase memory in `ClusterConfiguration` or YAML.

Delete when done:

```sh
oc delete raycluster --all -n ray-workshop
oc delete rayjob --all -n ray-workshop
```
