import pandas as pd
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
