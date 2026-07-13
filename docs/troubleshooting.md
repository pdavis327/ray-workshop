# Quick troubleshooting

Official: [Troubleshooting distributed workloads for users](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/troubleshooting-common-problems-with-distributed-workloads-for-users_distributed-workloads).

## Workbench creation

No hardware profiles in a Kueue-managed project:

- Set `disableKueue: false` in OdhDashboardConfig
- Create/enable a hardware profile with Local queue allocation pointing at a LocalQueue in the project

## CodeFlare auth

```sh
oc whoami --show-server
oc whoami --show-token
```

Use `skip_tls=False` by default. For self-signed clusters: `export RAY_WORKSHOP_SKIP_TLS=true`.

## RayJob stuck

```sh
oc describe rayjob <name> -n ray-workshop
oc get localqueue -n ray-workshop
```

In a notebook:

```python
from codeflare_sdk import list_local_queues
list_local_queues("ray-workshop")
```

## Logs

```python
job.status()
job.logs()
```

Or:

```sh
oc logs -n ray-workshop -l ray.io/node-type=head -c ray-head --tail=200
```

## Reset

```sh
oc delete rayjob --all -n ray-workshop
oc delete raycluster --all -n ray-workshop
```
