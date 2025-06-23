#!/usr/bin/env python3
"""
Scan all Jupyter notebooks in the Notebooks/ directory and ensure each one has
the required top‐level metadata fields (`kernelspec` and `language_info`).
If missing, insert default values. Overwrites the original notebooks in place.
"""

import json
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
    """Load a notebook, ensure metadata, and write back if modified."""
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    meta = nb.setdefault("metadata", {})
    changed = False

    # Inject kernelspec if missing or incomplete
    ks = meta.get("kernelspec", {})
    for key, val in DEFAULT_METADATA["kernelspec"].items():
        if ks.get(key) != val:
            ks[key] = val
            changed = True
    meta["kernelspec"] = ks

    # Inject language_info if missing or incomplete
    li = meta.get("language_info", {})
    for key, val in DEFAULT_METADATA["language_info"].items():
        if li.get(key) != val:
            li[key] = val
            changed = True
    meta["language_info"] = li

    if changed:
        # Write notebook back with pretty JSON formatting
        nb_path.write_text(json.dumps(nb, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
        print(f"Updated metadata in {nb_path}")
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