# 5. Troubleshooting

<p align="center">
<a href="/docs/04-observe-and-manage.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/README.md">Next</a>
</p>

### Objectives (~5 min)

- Quick fixes for common workshop failures.

### Common issues

| Symptom | Fix |
|---------|-----|
| `TokenAuthentication` fails | Regenerate token; check server URL; `skip_tls=True` for self-signed |
| RayJob Pending | Wrong `local_queue`; Kueue quota exhausted; check `oc describe localqueue` |
| `ModuleNotFoundError: codeflare_sdk` | Use a workbench image with CodeFlare; or `pip install codeflare-sdk` |
| `FileNotFoundError` for iris.csv | Clone repo into workbench; run notebook from repo root |
| `wait_for_rayjob` import error | `pip install kubernetes` on workbench |
| Job FAILED in logs | Open head pod logs; check `runtime_env` pip deps |

### Reset between sessions

```sh
oc delete rayjob --all -n ray-workshop
oc delete raycluster --all -n ray-workshop
```

### Further reading

- [docs/troubleshooting.md](/docs/troubleshooting.md)
- [OpenShift AI distributed workloads troubleshooting](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html-single/working_with_distributed_workloads/)

<p align="center">
<a href="/docs/04-observe-and-manage.md">Prev</a>
&nbsp;&nbsp;&nbsp;
<a href="/README.md">Next</a>
</p>
