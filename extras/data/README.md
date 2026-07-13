# Workshop data

`iris.csv` is a **small bundled subset** (30 rows) of the classic Iris dataset for fast, offline-friendly labs. No S3 or internet access is required during the workshop.

Columns:

- `sepal_length`, `sepal_width`, `petal_length`, `petal_width` (floats)
- `species` (integer class label 0–2)

## Participant path (CodeFlare)

Scripts read `extras/data/iris.csv` from the cloned repo via CodeFlare `runtime_env.working_dir`. No ConfigMap or PVC setup is required.

## Facilitator YAML path (optional)

For `configs/facilitator/` smoke tests, create a ConfigMap manually:

```sh
oc create configmap ray-workshop-iris-data \
  --from-file=iris.csv=extras/data/iris.csv \
  -n ray-workshop --dry-run=client -o yaml | oc apply -f -
```
