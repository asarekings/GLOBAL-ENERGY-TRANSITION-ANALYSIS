#!/usr/bin/env python3
"""
Orchestrate automatic project setup:
1. Patch cost_model style
2. Patch plot_lcoe column inference
3. Generate notebooks with metadata
4. Patch notebook 04 to use df.head()
5. Update notebook metadata via nbformat
6. Copy config.yaml into Notebooks/
7. Install Python dependencies (including geospatial and network analysis)
8. Run the full pipeline and serve reports
"""

import subprocess
import shutil
from pathlib import Path

def run_step(desc, cmd):
    print(f"▶️  {desc}...")
    subprocess.run(cmd, check=True)

def main():
    # 1. Patch the cost_model style
    run_step("Patch cost_model.py style", ["python", "patch_cost_model.py"])

    # 2. Patch plot_lcoe to auto-infer missing columns
    run_step("Patch plot_lcoe column inference", ["python", "patch_cost_model_columns.py"])

    # 3. Regenerate notebooks with valid metadata
    run_step("Generate notebooks", ["python", "create_notebooks.py"])

    # 4. Patch notebook 04 to avoid KeyError
    run_step("Patch notebook 04 cell selection", ["python", "patch_notebook_04.py"])

    # 5. Update notebook metadata
    run_step("Update notebook metadata", ["python", "update_notebook_metadata_nbformat.py"])

    # 6. Copy config.yaml into Notebooks/
    cfg = Path("config.yaml")
    nb_dir = Path("Notebooks")
    if cfg.exists() and nb_dir.is_dir():
        shutil.copy(cfg, nb_dir / "config.yaml")
        print("✅ Copied config.yaml to Notebooks/")

    # 7. Install Python dependencies, including geospatial and network analysis libs
    deps = [
        "nbformat",
        "seaborn",
        "folium",
        "geopandas",
        "networkx",
        "scipy"
    ]
    run_step("Install Python dependencies", ["pip", "install"] + deps)

    # 8. Run the full pipeline (ingest, preprocess, simulate, convert & serve)
    run_step("Run full pipeline", ["python", "run_local.py"])

    print("🎉 Bootstrapping complete. Reports are live at http://localhost:8000")

if __name__ == "__main__":
    main()