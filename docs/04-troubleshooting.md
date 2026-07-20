# 4. Troubleshooting

<p align="center">
<a href="/docs/03-ray-train.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/README.md">Next</a>
</p>

Official guide: [Troubleshooting common problems with distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/troubleshooting-common-problems-with-distributed-workloads-for-users_distributed-workloads).

### Common issues

| Symptom | Fix |
|---------|-----|
| No hardware profiles when creating workbench | Run `setup.sh -s 1` for `cpu-local-queue`; enable `disableKueue: false` |
| `CERTIFICATE_VERIFY_FAILED` on API | Use Console token; set `verify_ssl=False` on `AuthConfig` for lab self-signed certs |
| `system:anonymous` / forbidden | Fresh Console token; re-run auth cell after kernel restart (not workbench SA) |
| RayCluster Suspended / no pods | Wrong `local_queue`; missing GPU quota; check `list_local_queues()` and `oc describe workload` |
| `Default Local Queue not found` | Facilitator: run `setup.sh -s 1` or create LocalQueue in project |
| `local_queue provided does not exist` | Match `local_queue=` to a real LocalQueue (workshop default: `ray-workshop-queue`) |
| Job stuck PENDING on Ray | Check `client.get_job_logs()`; GPU/`num_workers` mismatch inside the script |
| Ray Train PENDING / never starts | `ScalingConfig.num_workers` must match GPU Ray workers (workshop: 2); do not use demo `num_workers=3` on a 2-GPU cluster |
| Head `BackOff` / `OOMKilled` (exit 137) | Raise `head_memory_limits` (MODH Ray image often needs ≥8Gi); `cluster.down()` and re-apply |
| `ModuleNotFoundError: codeflare_sdk` | Use Standard Data Science image or `pip install codeflare-sdk` |
| Forgot to tear down | `cluster.down()` or `oc delete raycluster --all -n ray-workshop` |

### Reset between sessions

```sh
oc delete raycluster --all -n ray-workshop
oc delete rayjob --all -n ray-workshop
```

### Further reading

- [docs/troubleshooting.md](/docs/troubleshooting.md)

<p align="center">
<a href="/docs/03-ray-train.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/README.md">Next</a>
</p>
