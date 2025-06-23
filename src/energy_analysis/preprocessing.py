import yaml, pandas as pd, numpy as np
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
