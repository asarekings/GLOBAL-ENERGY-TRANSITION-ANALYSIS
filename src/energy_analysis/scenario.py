import yaml, pandas as pd
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
