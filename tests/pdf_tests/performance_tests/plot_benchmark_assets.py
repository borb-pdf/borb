#!/usr/bin/env python3

import json
import pathlib
import typing

import matplotlib.pyplot as plt  # type: ignore[import-not-found]


def main() -> None:
    """Load per-commit benchmark results and create a stacked bar chart."""

    results_dir: pathlib.Path = pathlib.Path(__file__).resolve().parent / "assets"
    output_file: pathlib.Path = (
        pathlib.Path(__file__).resolve().parent / "assets" / "assets.png"
    )

    result_files: typing.List[pathlib.Path] = sorted(
        results_dir.glob("*.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not result_files:
        raise SystemExit(f"No JSON benchmark files found in {results_dir}")

    commits: typing.List[str] = []
    measurements_by_commit: typing.List[typing.Dict[str, float]] = []
    measurement_names: typing.List[str] = []

    for result_file in result_files:
        with result_file.open("r", encoding="utf-8") as file:
            result: typing.Dict[str, typing.Dict[str, float]] = json.load(file)

        commits.append(result_file.stem)

        for measurement_name, stats in result.items():
            if measurement_name not in measurement_names:
                measurement_names.append(measurement_name)

        measurements_by_commit.append(
            {
                measurement_name: float(stats["median"])
                for measurement_name, stats in result.items()
            }
        )

    positions: typing.List[int] = list(range(len(commits)))
    left: typing.List[float] = [0.0] * len(commits)

    figure, axis = plt.subplots(figsize=(12, max(5, len(commits) * 0.55)))

    for measurement_name in measurement_names:
        values: typing.List[float] = [
            measurements.get(measurement_name, 0.0)
            for measurements in measurements_by_commit
        ]

        axis.barh(
            positions,
            values,
            left=left,
            height=0.65,
            label=measurement_name,
        )

        left = [accumulated + value for accumulated, value in zip(left, values)]

    axis.set_yticks(positions)
    axis.set_yticklabels(commits)
    axis.invert_yaxis()
    axis.set_xlabel("Median execution time (seconds)")
    axis.set_title("Import/Layout/Write Benchmark")
    axis.grid(axis="x", alpha=0.25)
    axis.set_axisbelow(True)
    axis.legend(title="Measurement")
    figure.tight_layout()

    output_file.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_file, dpi=160, bbox_inches="tight")

    print(f"Loaded {len(result_files)} benchmark files.")
    print(f"Chart written to {output_file}")

    plt.show()


if __name__ == "__main__":
    main()
