#!/usr/bin/env python3
"""
Scan all Jupyter notebooks in the Notebooks/ directory and ensure each one has
the required top‐level metadata fields (`kernelspec` and `language_info`).
Uses nbformat to robustly parse/write notebooks, handling minor JSON issues.
Overwrites the original notebooks in place.
"""

import nbformat
from pathlib import Path

# Default metadata to inject if missing
DEFAULT_METADATA = {
    "kernelspec": {
        "name": "python3",
        "display_name": "Python 3",
        "language": "python"
    },
    "language_info": {
        "name": "python",
        "version": "3.8",
        "mimetype": "text/x-python",
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py"
    }
}

def ensure_metadata(nb_path: Path):
    try:
        nb = nbformat.read(str(nb_path), as_version=4)
    except Exception as e:
        print(f"ERROR reading {nb_path}: {e}")
        return

    meta = nb.metadata
    changed = False

    # kernelspec
    ks = getattr(meta, 'kernelspec', {}) if isinstance(meta, dict) else {}
    for key, val in DEFAULT_METADATA["kernelspec"].items():
        if ks.get(key) != val:
            ks[key] = val
            changed = True
    meta['kernelspec'] = ks

    # language_info
    li = getattr(meta, 'language_info', {}) if isinstance(meta, dict) else {}
    for key, val in DEFAULT_METADATA["language_info"].items():
        if li.get(key) != val:
            li[key] = val
            changed = True
    meta['language_info'] = li

    if changed:
        try:
            nbformat.write(nb, str(nb_path))
            print(f"Updated metadata in {nb_path}")
        except Exception as e:
            print(f"ERROR writing {nb_path}: {e}")
    else:
        print(f"No update needed for {nb_path}")

def main():
    notebooks_dir = Path("Notebooks")
    if not notebooks_dir.exists():
        print("Error: Notebooks/ directory not found.")
        return

    ipynb_files = list(notebooks_dir.glob("*.ipynb"))
    if not ipynb_files:
        print("No .ipynb files found in Notebooks/.")
        return

    for nb_path in ipynb_files:
        ensure_metadata(nb_path)

if __name__ == "__main__":
    main()