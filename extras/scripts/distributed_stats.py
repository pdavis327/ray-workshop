"""Distributed compute lab: partition Iris rows across Ray workers.

Each worker computes summary statistics for its partition. No ML frameworks
required — demonstrates Ray Core task fan-out on KubeRay.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import ray


def _load_rows(path: Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "petal_length": float(row["petal_length"]),
                    "petal_width": float(row["petal_width"]),
                    "species": float(row["species"]),
                }
            )
    return rows


@ray.remote
def summarize_partition(partition_id: int, rows: list[dict[str, float]]) -> dict:
    if not rows:
        return {"partition_id": partition_id, "count": 0}

    avg_petal_length = sum(r["petal_length"] for r in rows) / len(rows)
    avg_petal_width = sum(r["petal_width"] for r in rows) / len(rows)
    species_counts: dict[str, int] = {}
    for row in rows:
        key = str(int(row["species"]))
        species_counts[key] = species_counts.get(key, 0) + 1

    return {
        "partition_id": partition_id,
        "count": len(rows),
        "avg_petal_length": round(avg_petal_length, 4),
        "avg_petal_width": round(avg_petal_width, 4),
        "species_counts": species_counts,
    }


def _chunk(rows: list[dict[str, float]], num_chunks: int) -> list[list[dict[str, float]]]:
    if num_chunks < 1:
        num_chunks = 1
    chunk_size = max(1, (len(rows) + num_chunks - 1) // num_chunks)
    return [rows[i : i + chunk_size] for i in range(0, len(rows), chunk_size)]


def main() -> None:
    input_path = Path(os.environ.get("INPUT_PATH", "extras/data/iris.csv"))
    num_partitions = int(os.environ.get("NUM_PARTITIONS", "4"))

    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    rows = _load_rows(input_path)
    partitions = _chunk(rows, num_partitions)
    print(f"Loaded {len(rows)} rows, submitting {len(partitions)} partitions")

    ray.init()
    futures = [
        summarize_partition.remote(idx, partition)
        for idx, partition in enumerate(partitions)
    ]
    results = ray.get(futures)
    print(json.dumps(results, indent=2))
    print(f"Aggregated row count: {sum(r['count'] for r in results)}")


if __name__ == "__main__":
    main()
