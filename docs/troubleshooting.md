# Quick troubleshooting

Official: [Troubleshooting distributed workloads for users](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/troubleshooting-common-problems-with-distributed-workloads-for-users_distributed-workloads).

## Workbench creation

No hardware profiles in a Kueue-managed project:

- Set `disableKueue: false` in OdhDashboardConfig
- Create/enable a hardware profile with Local queue allocation pointing at a LocalQueue in the project

## CodeFlare auth

Get **server** and **token** from OpenShift Console → your username → **Copy login command** → Display token.

Do not use `oc whoami --show-token` inside the workbench — that is the workbench **service account**, which lacks permissions to create RayJobs.

In the notebook:

```python
from codeflare_sdk import TokenAuthentication

auth = TokenAuthentication(
    token="...",
    server="...",
    skip_tls=True,  # lab clusters with self-signed certs; use False when trusted
)
auth.login()
```

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
