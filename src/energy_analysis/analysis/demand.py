import pandas as pd
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
