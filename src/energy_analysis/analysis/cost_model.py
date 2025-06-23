"""Plot levelized cost of energy with robust column inference."""
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from energy_analysis.analysis.learning_curve import learning_curve

def plot_lcoe(
    df: pd.DataFrame,
    tech_col: str = "technology",
    cost_col: str = "capex",
    year_col: str = "year",
    cum_col: str = "cumulative_capacity",
    outdir: str = "figures"
):
    # Ensure output directory exists
    Path(outdir).mkdir(exist_ok=True)
    cols = df.columns.tolist()
    print(f"ℹ️  DataFrame columns detected: {cols}")

    # Helper to match column patterns case‐insensitively
    def find_first(patterns):
        for pat in patterns:
            matches = [c for c in cols if pat in c.lower()]
            if matches:
                return matches[0]
        return None

    # Infer technology column
    if tech_col not in cols:
        inferred = find_first(["tech", "name"])
        if inferred:
            old = tech_col
            tech_col = inferred
            print(f"⚠️  Inferred tech column '{tech_col}' (was '{old}')")
        else:
            print("⚠️  No tech-like column found, grouping all data under a single category.")
            df["_all_tech_"] = "all"
            tech_col = "_all_tech_"

    # Infer cost column
    if cost_col not in cols:
        inferred = find_first(["cost", "capex", "price"])
        if inferred:
            old = cost_col
            cost_col = inferred
            print(f"⚠️  Inferred cost column '{cost_col}' (was '{old}')")
        else:
            numeric = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
            if numeric:
                old = cost_col
                cost_col = numeric[0]
                print(f"⚠️  Using first numeric column '{cost_col}' for cost (was '{old}')")
            else:
                raise KeyError("No suitable numeric column found for cost_col.")

    # Infer year column
    if year_col not in cols:
        inferred = find_first(["year", "date"])
        if inferred:
            old = year_col
            year_col = inferred
            print(f"⚠️  Inferred year column '{year_col}' (was '{old}')")
        else:
            numeric = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
            if numeric:
                old = year_col
                year_col = numeric[0]
                print(f"⚠️  Using first numeric column '{year_col}' for year (was '{old}')")
            else:
                raise KeyError("No suitable column found for year_col.")

    # Apply a seaborn theme
    sns.set_theme(style="darkgrid")

    # Create the plot
    fig, ax = plt.subplots(figsize=(9, 6))
    for tech, group in df.groupby(tech_col):
        x = group[year_col]
        y = group[cost_col]
        # If cumulative capacity is available, apply learning curve adjustment
        if cum_col in group:
            y = learning_curve(y, group[cum_col])
        ax.plot(x, y, marker="o", label=str(tech))

    ax.set_xlabel(year_col)
    ax.set_ylabel(cost_col)
    ax.set_title("Levelized Cost of Energy")
    ax.legend()

    # Save figure
    out_file = Path(outdir) / "lcoe_plot.png"
    fig.savefig(out_file, dpi=300, bbox_inches="tight")
    print(f"🖼️  Saved LCOE plot to {out_file}")