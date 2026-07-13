# Optional shell aliases for the workshop namespace.

```sh
alias rw-ns='oc project ray-workshop'
alias rw-jobs='oc get rayjob -n ray-workshop'
alias rw-clusters='oc get raycluster -n ray-workshop'
alias rw-pods='oc get pods -n ray-workshop -l ray.io/is-ray-node=yes'
alias rw-logs='oc logs -n ray-workshop -l ray.io/node-type=head -c ray-head --tail=100'
```
