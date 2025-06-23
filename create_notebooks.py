#!/usr/bin/env python3
"""
Regenerate all Jupyter notebooks with proper top‐level metadata and cells.
This will overwrite existing notebooks in Notebooks/ to ensure nbformat validity.
"""

import nbformat
from pathlib import Path

# Common metadata for all notebooks
NB_METADATA = {
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

# Define the content of each notebook
NOTEBOOKS = {
    "01_data_ingest.ipynb": [
        {"cell_type": "markdown", "source": "# 01_data_ingest\n\nDownload and cache all raw datasets with versioning."},
        {"cell_type": "code", "source": "from energy_analysis.data_ingest import main\n\nif __name__ == '__main__':\n    main()"},
        {"cell_type": "markdown", "source": "**Output**: Check `data/raw/` for downloaded CSV files."}
    ],
    "02_preprocessing.ipynb": [
        {"cell_type": "markdown", "source": "# 02_preprocessing\n\nClean and transform raw data to analysis-ready tables."},
        {"cell_type": "code", "source": "from energy_analysis.preprocessing import main\n\nif __name__ == '__main__':\n    main()"},
        {"cell_type": "markdown", "source": "**Output**: Cleaned CSVs in `data/processed/`."}
    ],
    "03_demand_side_analysis.ipynb": [
        {"cell_type": "markdown", "source": "# 03_demand_side_analysis\n\nExplore energy consumption and efficiency measures on the demand side."},
        {"cell_type": "code", "source": (
            "import yaml\n"
            "from energy_analysis.analysis.demand import load_consumption, plot_global_demand\n\n"
            "# Load processed data\n"
            "cfg = yaml.safe_load(open('config.yaml'))\n"
            "df = load_consumption(cfg['data']['processed_dir'])\n\n"
            "# Generate and display plot\n"
            "plot_global_demand(df, outdir='figures')\n"
            "df.head()"
        )}
    ],
    "04_levelized_cost_modeling.ipynb": [
        {"cell_type": "markdown", "source": "# 04_levelized_cost_modeling\n\nModel levelized cost of energy (LCOE) for key technologies."},
        {"cell_type": "code", "source": (
            "import yaml\n"
            "import pandas as pd\n"
            "from energy_analysis.analysis.cost_model import plot_lcoe\n\n"
            "# Load processed data\n"
            "cfg = yaml.safe_load(open('config.yaml'))\n"
            "df = pd.read_csv(f\"{cfg['data']['processed_dir']}/sample_energy.csv\")\n\n"
            "# Generate LCOE forecasts and plot\n"
            "plot_lcoe(df, tech_col='technology', cost_col='capex', year_col='year', outdir='figures')\n"
            "df[['year','technology','capex']].head()"
        )}
    ],
    "05_scenario_simulation.ipynb": [
        {"cell_type": "markdown", "source": "# 05_scenario_simulation\n\nRun Monte Carlo or sensitivity analyses across multiple policy/economic scenarios."},
        {"cell_type": "code", "source": (
            "import yaml\n"
            "import pandas as pd\n"
            "from energy_analysis.scenario import run_scenarios\n\n"
            "# Load config & processed data\n"
            "cfg = yaml.safe_load(open('config.yaml'))\n"
            "df = pd.read_csv(f\"{cfg['data']['processed_dir']}/sample_energy.csv\")\n\n"
            "# Run scenarios\n"
            "results = run_scenarios(df, cfg['scenarios'])\n"
            "results.head()"
        )},
        {"cell_type": "code", "source": (
            "# Save scenario results\n"
            "results.to_csv('data/processed/scenario_results.csv', index=False)\n"
            "print('Wrote data/processed/scenario_results.csv')"
        )}
    ],
    "06_visualization_and_storytelling.ipynb": [
        {"cell_type": "markdown", "source": "# 06_visualization_and_storytelling\n\nEnhanced Narrative & Styling"},
        {"cell_type": "code", "source": (
            "import yaml\n"
            "import pandas as pd\n"
            "import seaborn as sns\n"
            "import plotly.express as px\n"
            "from energy_analysis.visualization import plot_scenarios\n\n"
            "# Load data\n"
            "df = pd.read_csv('data/processed/scenario_results.csv')\n\n"
            "# Static Seaborn plot\n"
            "sns.set_theme(style='whitegrid', palette='muted')\n"
            "plot_scenarios('data/processed/scenario_results.csv', outdir='figures')\n\n"
            "# Interactive Plotly chart\n"
            "fig = px.line(df, x='year', y='cons_adj', color='scenario',\n"
            "              title='Scenario-adjusted Energy Consumption (Interactive)')\n"
            "fig.update_layout(template='plotly_white')\n"
            "fig.show()"
        )},
        {"cell_type": "markdown", "source": (
            "## Key Insights\n"
            "- **Baseline:** Moderate growth tempered by carbon pricing and efficiency gains.\n"
            "- **High Policy:** Strong reductions driven by aggressive efficiency and electrification.\n"
            "- **Low Policy:** Higher consumption due to weak policy levers and slow efficiency.\n"
            "- **Accelerated Tech:** Rapid uptake yields the lowest adjusted demand by 2050.\n"
        )}
    ],
}

def main():
    nb_dir = Path("Notebooks")
    nb_dir.mkdir(exist_ok=True)
    for fname, cells in NOTEBOOKS.items():
        path = nb_dir / fname
        nb = nbformat.v4.new_notebook()
        nb.metadata.update(NB_METADATA)
        # Add cells
        for cell in cells:
            if cell["cell_type"] == "markdown":
                nb.cells.append(nbformat.v4.new_markdown_cell(cell["source"]))
            else:
                nb.cells.append(nbformat.v4.new_code_cell(cell["source"]))
        # Write notebook
        nbformat.write(nb, str(path))
        print(f"Written {path}")

if __name__ == "__main__":
    main()