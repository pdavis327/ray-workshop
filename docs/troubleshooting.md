# Quick troubleshooting

Official: [Troubleshooting distributed workloads for users](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/troubleshooting-common-problems-with-distributed-workloads-for-users_distributed-workloads).

## Workbench creation

No hardware profiles in a Kueue-managed project:

- Set `disableKueue: false` in OdhDashboardConfig
- Create/enable a hardware profile with Local queue allocation pointing at a LocalQueue in the project

## CodeFlare auth

Get **server** and **token** from OpenShift Console → your username → **Copy login command** → Display token.

Do not use `oc whoami --show-token` inside the workbench — that is the workbench **service account**, which lacks permissions to create RayClusters.

In the notebook:

```python
from kube_authkit import AuthConfig, get_k8s_client
from codeflare_sdk import set_api_client

auth_config = AuthConfig(
    method="openshift",
    k8s_api_host="...",
    token="...",
    verify_ssl=False,  # lab clusters with self-signed certs
)
set_api_client(get_k8s_client(config=auth_config))
```

## RayCluster stuck / no pods

```sh
oc get raycluster,workload -n ray-workshop
oc describe workload <name> -n ray-workshop
oc get localqueue -n ray-workshop
```

In a notebook:

```python
from codeflare_sdk import list_local_queues
list_local_queues("ray-workshop")
```

## Job status / logs

```python
client = cluster.job_client
client.get_job_status(submission_id)
client.get_job_logs(submission_id)
client.list_jobs()
```

Or:

```sh
oc logs -n ray-workshop -l ray.io/node-type=head -c ray-head --tail=200
```

## Reset

```sh
oc delete raycluster --all -n ray-workshop
# optional if any CR-based jobs exist:
oc delete rayjob --all -n ray-workshop
```
