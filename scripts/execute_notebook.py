from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NOTEBOOK = (
    ROOT
    / "output"
    / "jupyter-notebook"
    / "england_france_2026_third_place_analysis_v2.ipynb"
)


def main() -> None:
    parser = ArgumentParser(description="Execute a project notebook and save its outputs in place.")
    parser.add_argument("notebook", nargs="?", type=Path, default=DEFAULT_NOTEBOOK)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    notebook_path = args.notebook.resolve()
    with notebook_path.open("r", encoding="utf-8") as handle:
        notebook = nbformat.read(handle, as_version=4)

    client = NotebookClient(
        notebook,
        timeout=args.timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(ROOT)}},
    )
    client.execute()

    with notebook_path.open("w", encoding="utf-8") as handle:
        nbformat.write(notebook, handle)

    print(notebook_path)


if __name__ == "__main__":
    main()
