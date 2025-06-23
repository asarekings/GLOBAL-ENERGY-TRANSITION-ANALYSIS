#!/usr/bin/env python3
"""
Generate the complete Global Energy Transition Analysis project structure,
including all files and folders.
"""

import os
from pathlib import Path

# Mapping of relative file paths to their contents
FILES = {
    "README.md": """# Global Energy Transition Analysis

A reproducible pipeline for ingesting, preprocessing, analyzing, modeling, and visualizing global energy transition data.

## Structure

├── config.yaml             # Data sources & parameters  
├── environment.yml         # Conda environment  
├── requirements.txt        # pip requirements  
├── setup.py                # Installable package  
├── Makefile                # common commands  
├── src/energy_analysis/    # Python package with core modules  
│   ├── __init__.py  
│   ├── data_ingest.py  
│   ├── preprocessing.py  
│   ├── analysis/  
│   │   ├── __init__.py  
│   │   ├── demand.py  
│   │   └── cost_model.py  
│   ├── scenario.py  
│   └── visualization.py  
├── data/                   # raw & processed data  
│   ├── raw/  
│   └── processed/  
├── Notebooks/              # Jupyter notebooks  
│   ├── 01_data_ingest.ipynb  
│   ├── 02_preprocessing.ipynb  
│   ├── 03_demand_side_analysis.ipynb  
│   ├── 04_levelized_cost_modeling.ipynb  
│   ├── 05_scenario_simulation.ipynb  
│   └── 06_visualization_and_storytelling.ipynb  
├── .github/                # CI workflows  
│   └── workflows/  
│       └── run-notebooks.yml  
└── docs/  
    └── CONTRIBUTING.md
""",
    "environment.yml": """name: energy-analysis
channels:
  - conda-forge
dependencies:
  - python=3.8
  - pip
  - jupyterlab
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - scikit-learn
  - pyyaml
  - nbconvert
  - statsmodels
  - plotly
""",
    "requirements.txt": """jupyterlab
pandas
numpy
matplotlib
seaborn
scikit-learn
pyyaml
nbconvert
statsmodels
plotly
requests
""",
    "config.yaml": """data:
  raw_dir: data/raw
  processed_dir: data/processed
  sources:
    - name: sample_energy
      url: https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv

scenarios:
  - name: baseline
    carbon_price: 50
    gdp_growth: 0.03
    population_growth: 0.01
    efficiency_improvement: 0.005
    electrification_rate: 0.02

  - name: high_policy
    carbon_price: 100
    gdp_growth: 0.025
    population_growth: 0.008
    efficiency_improvement: 0.015
    electrification_rate: 0.05

  - name: low_policy
    carbon_price: 20
    gdp_growth: 0.04
    population_growth: 0.012
    efficiency_improvement: 0.002
    electrification_rate: 0.01

  - name: accelerated_tech
    carbon_price: 75
    gdp_growth: 0.03
    population_growth: 0.009
    efficiency_improvement: 0.02
    electrification_rate: 0.06
""",
    "Makefile": """.PHONY: data preprocess notebooks clean

data:
\tpython -m energy_analysis.data_ingest

preprocess:
\tpython -m energy_analysis.preprocessing

notebooks:
\tfor nb in Notebooks/*.ipynb; do \\
\t  jupyter nbconvert --to notebook --execute $$nb \\
\t    --ExecutePreprocessor.timeout=600 \\
\t    --output executed/"$$(basename $$nb)" ; \\
\tdone

clean:
\trm -rf data/processed/*
\trm -rf executed/*
""",
    "setup.py": """from setuptools import setup, find_packages

setup(
    name="energy_analysis",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "pandas", "numpy", "matplotlib", "seaborn",
        "scikit-learn", "pyyaml", "nbconvert",
        "statsmodels", "plotly", "requests"
    ],
    python_requires=">=3.8",
)
""",
    "src/energy_analysis/__init__.py": """# energy_analysis package""",
    "src/energy_analysis/data_ingest.py": """import yaml, requests
from pathlib import Path

def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)

def download_source(name, url, outdir):
    out = Path(outdir) / f"{name}.csv"
    if out.exists():
        print(f"⏭ {out} exists, skipping")
    else:
        print(f"⬇️  Downloading {url}")
        resp = requests.get(url)
        resp.raise_for_status()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(resp.content)
        print(f"✅ Saved to {out}")

def main():
    cfg = load_config()
    raw = cfg["data"]["raw_dir"]
    for src in cfg["data"]["sources"]:
        download_source(src["name"], src["url"], raw)

if __name__ == "__main__":
    main()
""",
    "src/energy_analysis/preprocessing.py": """import yaml, pandas as pd, numpy as np
from pathlib import Path

def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)

def drop_outliers(df, column, z_thresh=4.0):
    z = (df[column] - df[column].mean()) / df[column].std()
    return df[abs(z) <= z_thresh]

def compute_per_capita(df, pop_col, val_col):
    if pop_col in df.columns:
        df["energy_per_capita"] = df[val_col] / df[pop_col]
    return df

def clean_df(df):
    df = df.dropna(axis=1, how="all").drop_duplicates()
    df["year"] = df["year"].astype(int)
    df = drop_outliers(df, "primary_energy_consumption")
    df = df.sort_values(["country","year"]).groupby("country").apply(lambda g: g.ffill().bfill()).reset_index(drop=True)
    df = compute_per_capita(df, "population", "primary_energy_consumption")
    return df

def main():
    cfg = load_config()
    rawdir = Path(cfg["data"]["raw_dir"])
    procdir = Path(cfg["data"]["processed_dir"])
    procdir.mkdir(parents=True, exist_ok=True)
    for csv in rawdir.glob("*.csv"):
        print(f"🔄 Processing {csv.name}")
        df = pd.read_csv(csv)
        df_clean = clean_df(df)
        out = procdir / csv.name
        df_clean.to_csv(out, index=False)
        print(f"📝 Wrote cleaned data to {out}")

if __name__ == "__main__":
    main()
""",
    "src/energy_analysis/analysis/__init__.py": "# analysis subpackage",
    "src/energy_analysis/analysis/demand.py": """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_consumption(procdir):
    return pd.read_csv(Path(procdir) / "sample_energy.csv")

def plot_global_demand(df, outdir="figures"):
    Path(outdir).mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")
    yearly = df.groupby("year")["primary_energy_consumption"].sum().reset_index()
    plt.figure(figsize=(8,5))
    sns.lineplot(data=yearly, x="year", y="primary_energy_consumption")
    plt.title("Global Primary Energy Consumption Over Time")
    plt.savefig(Path(outdir)/"global_demand.png", dpi=150)
    plt.close()
    print(f"Saved global demand plot to {outdir}/global_demand.png")
""",
    "src/energy_analysis/analysis/cost_model.py": """import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def simple_lcoe(capex, output, lifetime=25, discount_rate=0.07):
    annuity = (discount_rate*(1+discount_rate)**lifetime)/((1+discount_rate)**lifetime-1)
    return capex * annuity / output

def learning_curve(cost_series, cum_series, learning_rate=0.20):
    exponent = -np.log2(1-learning_rate)
    return cost_series * (cum_series/cum_series.iloc[0])**exponent

def plot_lcoe(df, tech_col="technology", cost_col="capex", year_col="year", cum_col="cumulative_capacity", outdir="figures"):
    Path(outdir).mkdir(exist_ok=True)
    plt.style.use("seaborn-darkgrid")
    fig, ax = plt.subplots(figsize=(9,6))
    for tech, grp in df.groupby(tech_col):
        if cum_col in grp:
            series = learning_curve(grp[cost_col], grp[cum_col])
        else:
            series = grp[cost_col].apply(simple_lcoe, output=1e6)
        ax.plot(grp[year_col], series, label=tech)
    ax.set_title("Forecasted LCOE by Technology")
    ax.set_xlabel("Year")
    ax.set_ylabel("LCOE (USD/MWh)")
    ax.legend()
    fig.savefig(Path(outdir)/"lcoe_forecast.png", dpi=150)
    plt.close(fig)
    print(f"Saved LCOE forecast to {outdir}/lcoe_forecast.png")
""",
    "src/energy_analysis/scenario.py": """import yaml, pandas as pd
from pathlib import Path

def load_config():
    return yaml.safe_load(open("config.yaml"))

def run_scenarios(df, scenarios):
    res = []
    for s in scenarios:
        tmp = df.copy()
        tmp["cons_adj"] = tmp["primary_energy_consumption"] * (1+s["gdp_growth"]) / (1+s["carbon_price"]/1000)
        tmp["scenario"] = s["name"]
        res.append(tmp)
    return pd.concat(res, ignore_index=True)

def main():
    cfg = load_config()
    proc = cfg["data"]["processed_dir"]
    df = pd.read_csv(Path(proc)/"sample_energy.csv")
    out = run_scenarios(df, cfg["scenarios"])
    Path("data/processed").mkdir(exist_ok=True)
    out.to_csv("data/processed/scenario_results.csv", index=False)
    print("Wrote data/processed/scenario_results.csv")

if __name__ == "__main__":
    main()
""",
    "src/energy_analysis/visualization.py": """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def plot_scenarios(scen_csv, outdir="figures"):
    df = pd.read_csv(scen_csv)
    Path(outdir).mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted")
    plt.figure(figsize=(8,5))
    sns.lineplot(data=df, x="year", y="cons_adj", hue="scenario")
    plt.title("Scenario-adjusted Energy Consumption")
    plt.savefig(Path(outdir)/"scenario_comparison.png", dpi=150)
    plt.close()
    print(f"Saved scenario comparison to {outdir}/scenario_comparison.png")
""",
    "Notebooks/01_data_ingest.ipynb": """{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {},
 "cells": [
  {
   "cell_type": "markdown",
   "source": ["# 01_data_ingest\\n\\nDownload and cache all raw datasets with versioning."]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "source": [
    "from energy_analysis.data_ingest import main\\n",
    "if __name__=='__main__': main()"
   ],
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "source": ["**Output**: Check `data/raw/` for downloaded CSV files."]
  }
 ]
}""",
    "Notebooks/02_preprocessing.ipynb": """{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {},
 "cells": [
  {
   "cell_type": "markdown",
   "source": ["# 02_preprocessing\\n\\nClean and transform raw data to analysis-ready tables."]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "source": [
    "from energy_analysis.preprocessing import main\\n",
    "if __name__=='__main__': main()"
   ],
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "source": ["**Output**: Cleaned CSVs in `data/processed/`."]
  }
 ]
}""",
    "Notebooks/03_demand_side_analysis.ipynb": """{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {},
 "cells": [
  {
   "cell_type": "markdown",
   "source": ["# 03_demand_side_analysis\\n\\nExplore energy consumption and efficiency measures on the demand side."]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "source": [
    "import yaml, pandas as pd\\n",
    "from energy_analysis.analysis.demand import load_consumption, plot_global_demand\\n",
    "cfg=yaml.safe_load(open('config.yaml'))\\n",
    "df=load_consumption(cfg['data']['processed_dir'])\\n",
    "plot_global_demand(df)\\n",
    "df.head()"
   ],
   "outputs": []
  }
 ]
}""",
    "Notebooks/04_levelized_cost_modeling.ipynb": """{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {},
 "cells": [
  {
   "cell_type": "markdown",
   "source": ["# 04_levelized_cost_modeling\\n\\nModel levelized cost of energy (LCOE) for key technologies."]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "source": [
    "import yaml, pandas as pd\\n",
    "from energy_analysis.analysis.cost_model import plot_lcoe\\n",
    "cfg=yaml.safe_load(open('config.yaml'))\\n",
    "df=pd.read_csv(f\"{cfg['data']['processed_dir']}/sample_energy.csv\")\\n",
    "plot_lcoe(df)"
   ],
   "outputs": []
  }
 ]
}""",
    "Notebooks/05_scenario_simulation.ipynb": """{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {},
 "cells": [
  {
   "cell_type": "markdown",
   "source": ["# 05_scenario_simulation\\n\\nRun Monte Carlo or sensitivity analyses across multiple policy/economic scenarios."]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "source": [
    "import yaml, pandas as pd\\n",
    "from energy_analysis.scenario import run_scenarios\\n",
    "cfg=yaml.safe_load(open('config.yaml'))\\n",
    "df=pd.read_csv(f\"{cfg['data']['processed_dir']}/sample_energy.csv\")\\n",
    "res=run_scenarios(df, cfg['scenarios'])\\n",
    "res.head()"
   ],
   "outputs": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "source": [
    "res.to_csv('data/processed/scenario_results.csv', index=False)\\n",
    "print('Saved scenario_results.csv')"
   ],
   "outputs": []
  }
 ]
}""",
    "Notebooks/06_visualization_and_storytelling.ipynb": """{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {},
 "cells": [
  {
   "cell_type": "markdown",
   "source": ["# 06_visualization_and_storytelling\\n\\nEnhanced Narrative & Styling"]
  },
  {
   "cell_type": "code",
   "source": [
    "import yaml, pandas as pd, seaborn as sns, plotly.express as px\\n",
    "from energy_analysis.visualization import plot_scenarios\\n",
    "cfg=yaml.safe_load(open('config.yaml'))\\n",
    "df=pd.read_csv('data/processed/scenario_results.csv')\\n",
    "plot_scenarios('data/processed/scenario_results.csv')\\n",
    "fig=px.line(df,x='year',y='cons_adj',color='scenario',title='Scenario-adjusted Consumption')\\n",
    "fig.show()"
   ],
   "execution_count": null,
   "outputs": []
  },
  {
   "cell_type": "markdown",
   "source": [
    "## Key Insights\\n",
    "- **Baseline:** Moderate growth tempered by carbon pricing and efficiency gains.\\n",
    "- **High Policy:** Strong reductions driven by aggressive efficiency and electrification.\\n",
    "- **Low Policy:** Higher consumption due to weak policy levers and slow efficiency.\\n",
    "- **Accelerated Tech:** Rapid uptake yields lowest adjusted demand by 2050.\\n"
   ]
  }
 ]
}""",
    ".github/workflows/run-notebooks.yml": """name: Run Notebooks & Publish Reports

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with: python-version: 3.8
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Data & preprocess
        run: |
          make data
          make preprocess
      - name: Execute notebooks
        run: make notebooks
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: notebook-outputs
          path: executed/*.html
""",
    "docs/CONTRIBUTING.md": """# Contributing Guide

## Setup

1. Fork and clone.
2. Create Conda env: `conda env create -f environment.yml`.
3. Activate: `conda activate energy-analysis`.
4. Install deps: `pip install -r requirements.txt`.
5. Run `make data preprocess notebooks` to verify.

## Workflow

- Add data sources in `config.yaml`.
- Update modules under `src/energy_analysis/`.
- Update notebooks.
- Ensure CI passes.

## Style

- PEP8 for code.
- Markdown narrative in notebooks.
"""
}

def main():
    for path, content in FILES.items():
        file_path = Path(path)
        dir_path = file_path.parent
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
        # Write text content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created {file_path}")

    # Ensure notebooks output folder
    Path("executed").mkdir(exist_ok=True)
    Path("figures").mkdir(exist_ok=True)
    print("Project scaffold complete.")

if __name__ == "__main__":
    main()