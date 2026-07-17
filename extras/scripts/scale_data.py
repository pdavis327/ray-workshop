"""Ray Data lab: read Iris CSV, add petal area, write Parquet.

Defaults suit CodeFlare job_client runtime_env (repo packaged as working_dir):
  INPUT_PATH=extras/data/iris.csv
  OUTPUT_DIR=/tmp/ray-workshop-output/iris
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import ray


def _paths() -> tuple[Path, Path]:
    input_path = Path(os.environ.get("INPUT_PATH", "extras/data/iris.csv"))
    output_dir = Path(os.environ.get("OUTPUT_DIR", "/tmp/ray-workshop-output/iris"))
    return input_path, output_dir


def compute_area(batch: dict[str, Any]) -> dict[str, Any]:
    batch["petal_area"] = batch["petal_length"] * batch["petal_width"]
    return batch


def main() -> None:
    input_path, output_dir = _paths()
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    print(f"Reading {input_path}")
    ds = ray.data.read_csv(str(input_path))
    transformed = ds.map_batches(compute_area, batch_size=8)

    for batch in transformed.iter_batches(batch_size=4):
        print(batch)

    output_dir.mkdir(parents=True, exist_ok=True)
    out = f"local://{output_dir.resolve()}"
    print(f"Writing Parquet to {out}")
    transformed.write_parquet(out)
    files = list(output_dir.glob("*.parquet"))
    print(f"Done. Wrote {len(files)} parquet file(s) to {output_dir}")


if __name__ == "__main__":
    main()
