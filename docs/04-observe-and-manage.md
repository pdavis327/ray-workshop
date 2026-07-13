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

1. Open `extras/notebooks/04-observe-and-manage.ipynb`.
2. Run `list_local_queues()` and `view_clusters()`.
3. Use Open Ray Dashboard / View Jobs from the widget UI.

### Console (facilitator demo)

| View | Highlight |
|------|-----------|
| Projects → ray-workshop | Workbench + workloads |
| RayJobs | CRs created by CodeFlare |
| Pods | `ray-head`, `ray-worker` during jobs |
| LocalQueue | Kueue admission |

```sh
oc get rayjob,raycluster,pods -n ray-workshop
oc describe localqueue ray-workshop-queue -n ray-workshop
```

### Key message

> Data scientists stay in Jupyter. OpenShift AI and KubeRay handle Kubernetes, quotas, and cluster lifecycle.

<p align="center">
<a href="/docs/03-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/05-troubleshooting.md">Next</a>
</p>
