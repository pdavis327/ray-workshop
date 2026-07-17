# 4. Observe and manage

<p align="center">
<a href="/docs/03-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/05-troubleshooting.md">Next</a>
</p>

### Objectives (~10 min)

- Use CodeFlare widgets per [Managing Ray clusters from within a Jupyter notebook](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/running-ray-based-distributed-workloads_distributed-workloads#managing-ray-clusters-from-within-a-jupyter-notebook_running-ray-based-distributed-workloads).
- Connect notebook tools to OpenShift AI console views.

### Hands-on

1. In JupyterLab, open `ray-workshop/extras/notebooks/04-observe-and-manage.ipynb`.
2. When you reach the auth cell, paste your OpenShift server URL and token (same as [Topic 2](/docs/02-ray-data-cluster.md#hands-on)).
3. Run all cells — `list_local_queues()` and `view_clusters()`.
4. Use Open Ray Dashboard / View Jobs from the widget UI.

Tip: leave a Topic 2 or 3 cluster up (skip `cluster.down()`) so `view_clusters()` has something to show.

### Console (facilitator demo)

| View | Highlight |
|------|-----------|
| Projects → ray-workshop | Workbench + RayClusters |
| Ray Dashboard → Jobs | Jobs from `job_client` |
| Pods | `ray-head`, `ray-worker` while cluster is up |
| LocalQueue | Kueue admission for the RayCluster |

```sh
oc get raycluster,pods -n ray-workshop
oc describe localqueue ray-workshop-queue -n ray-workshop
```

### Key message

> Data scientists stay in Jupyter. OpenShift AI and KubeRay handle Kubernetes and quotas. Tear clusters down when finished.

<p align="center">
<a href="/docs/03-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/05-troubleshooting.md">Next</a>
</p>
