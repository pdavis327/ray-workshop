# Quick troubleshooting

## CodeFlare auth fails

- Regenerate token: `oc whoami --show-token`
- Confirm server URL: `oc whoami --show-server`
- Self-signed clusters: notebooks use `skip_tls=True` in `workshop_common.login()`

## RayJob stuck in Pending

```sh
oc describe rayjob <name> -n ray-workshop
oc get events -n ray-workshop --sort-by='.lastTimestamp' | tail -20
oc get workloads -n ray-workshop  # Kueue admitted workloads
oc describe localqueue ray-workshop-queue -n ray-workshop
```

Common causes:

- Wrong `local_queue` in notebook (must be `ray-workshop-queue`)
- Kueue quota exhausted on the ClusterQueue
- Insufficient cluster CPU/memory for head + workers

## No workers

- Check CPU quotas and `ManagedClusterConfig` resource settings in `workshop_common.py`.
- Confirm LocalQueue exists: `oc get localqueue -n ray-workshop`.

## Logs

```sh
oc logs -n ray-workshop -l ray.io/node-type=head -c ray-head --tail=200
oc logs -n ray-workshop -l ray.io/node-type=worker -c ray-worker --tail=100
```

Or use **View Jobs** / Ray dashboard from `04-observe-and-manage.ipynb`.

## Reset between sessions

```sh
oc delete rayjob --all -n ray-workshop
oc delete raycluster --all -n ray-workshop
```
