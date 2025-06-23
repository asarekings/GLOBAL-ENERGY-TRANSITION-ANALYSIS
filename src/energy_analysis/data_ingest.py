import yaml, requests
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
