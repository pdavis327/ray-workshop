# 5. Troubleshooting

<p align="center">
<a href="/docs/04-observe-and-manage.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/README.md">Next</a>
</p>

Official guide: [Troubleshooting common problems with distributed workloads](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_distributed_workloads/troubleshooting-common-problems-with-distributed-workloads-for-users_distributed-workloads).

### Common issues

| Symptom | Fix |
|---------|-----|
| No hardware profiles when creating workbench | Run `setup.sh -s 1` for `cpu-local-queue`; enable `disableKueue: false` |
| `TokenAuthentication` fails | Regenerate token; check server URL; try `RAY_WORKSHOP_SKIP_TLS=true` |
| RayJob Pending | Wrong `local_queue`; check `list_local_queues()` and `oc describe localqueue` |
| `Default Local Queue not found` | Facilitator: run `setup.sh -s 1` or create LocalQueue in project |
| `local_queue provided does not exist` | Match `RAY_WORKSHOP_LOCAL_QUEUE` to a real LocalQueue name |
| `ModuleNotFoundError: codeflare_sdk` | Use Standard Data Science image or `pip install codeflare-sdk` |
| Job FAILED | `job.logs()` or head pod logs; check `runtime_env` pip deps |

### Reset between sessions

```sh
oc delete rayjob --all -n ray-workshop
oc delete raycluster --all -n ray-workshop
```

### Further reading

- [docs/troubleshooting.md](/docs/troubleshooting.md)

<p align="center">
<a href="/docs/04-observe-and-manage.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/README.md">Next</a>
</p>
