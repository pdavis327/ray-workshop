# Facilitator-only manifests

These YAML files are **not** part of the participant workshop path. Participants submit jobs with the **CodeFlare SDK** from a workbench notebook.

Facilitators may use these manifests to:

- Smoke-test KubeRay before a session (create PVC + ConfigMaps manually, then `oc apply -f ray-data/rayjob-scale-data.yaml`)
- Debug cluster issues without a workbench
- Show customers what CodeFlare creates under the hood (`oc get rayjob -o yaml`)

Participant labs live in `extras/notebooks/`.
