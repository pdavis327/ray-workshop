# 4. Observe and manage

<p align="center">
<a href="/docs/03-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/05-troubleshooting.md">Next</a>
</p>

### Objectives (~10 min)

- Use CodeFlare widgets to inspect Ray workloads.
- Connect notebook experience to **OpenShift AI platform views** (the sell).

### Hands-on

1. Open `extras/notebooks/04-observe-and-manage.ipynb`.
2. Run `list_local_queues()` and `view_clusters()`.
3. Use **Open Ray Dashboard** / **View Jobs** from the widget UI.

### Show in the OpenShift console

Walk customers through:

| View | What to highlight |
|------|-------------------|
| **Projects → ray-workshop** | Workbench + workloads in one place |
| **RayJobs** | CRs CodeFlare created from the notebook |
| **Pods** | `ray-head`, `ray-worker` while jobs run |
| **LocalQueue** | Kueue admission for the project |

```sh
oc get rayjob,raycluster,pods -n ray-workshop
oc describe localqueue ray-workshop-queue -n ray-workshop
```

### Key message

> "Your data scientists stay in Jupyter. OpenShift AI and KubeRay handle Kubernetes, scaling, quotas, and cleanup."

### Checklist

- [ ] `view_clusters()` lists recent clusters or shows empty after teardown.
- [ ] Ray dashboard opens from the notebook widget.
- [ ] Customer can find RayJob status in OpenShift AI / console search.

<p align="center">
<a href="/docs/03-distributed-compute.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/docs/05-troubleshooting.md">Next</a>
</p>
