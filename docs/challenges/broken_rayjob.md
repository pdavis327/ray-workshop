# Challenge: fix a broken RayJob

Optional exercise (~10 min) for facilitators or advanced participants.

## Scenario A — notebook (participant path)

In `02-ray-data-rayjob.ipynb`, deliberately set:

```python
LOCAL_QUEUE = "does-not-exist-queue"
```

before submitting the job.

## Your task

1. Submit the job and observe the failure (`job.status()` stays Pending / does not SUCCEEDED).
2. Inspect status:

```sh
oc describe rayjob ray-workshop-scale-data -n ray-workshop
oc describe localqueue -n ray-workshop
```

3. Fix `LOCAL_QUEUE` back to `ray-workshop-queue` and resubmit.

## Scenario B — YAML (facilitator only)

`configs/challenges/broken-rayjob.yaml` uses a bad Kueue queue annotation and undersized head memory.

1. Apply: `oc apply -f configs/challenges/broken-rayjob.yaml`
2. Observe failure mode (`oc describe rayjob`, events, pod status).
3. Fix queue → `ray-workshop-queue`, head memory → at least `2Gi`, re-apply.

## Solution hints

- Kueue events mention unknown or inactive queue names.
- OOMKilled head pod → increase memory in `ManagedClusterConfig` or YAML.

Delete when done:

```sh
oc delete rayjob ray-workshop-broken -n ray-workshop
oc delete rayjob ray-workshop-scale-data -n ray-workshop
```
