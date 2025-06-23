#!/usr/bin/env python3
"""
Patch plot_lcoe to auto-infer missing columns if provided keys are not in the DataFrame.
This prevents KeyError when column names differ in the CSV.
"""
import re
from pathlib import Path

file = Path("src/energy_analysis/analysis/cost_model.py")
if not file.exists():
    print("cost_model.py not found, skipping column-inference patch.")
    exit(1)

text = file.read_text(encoding="utf-8")

# After the function signature, inject auto-inference boilerplate
pattern = r"(def plot_lcoe\(.*\):\n)"
inference = r"""\1    # --- auto-infer missing columns ---
    cols = df.columns.tolist()
    if tech_col not in cols:
        candidates = [c for c in cols if "tech" in c.lower()]
        if candidates:
            old = tech_col
            tech_col = candidates[0]
            print(f"⚠️  Inferred technology column: '{tech_col}' (was '{old}')")
        else:
            raise KeyError(f"Column '{tech_col}' not found and no tech-like column available.")
    if cost_col not in cols:
        candidates = [c for c in cols if "cost" in c.lower()]
        if candidates:
            old = cost_col
            cost_col = candidates[0]
            print(f"⚠️  Inferred cost column: '{cost_col}' (was '{old}')")
        else:
            raise KeyError(f"Column '{cost_col}' not found and no cost-like column available.")
    if year_col not in cols:
        candidates = [c for c in cols if "year" in c.lower()]
        if candidates:
            old = year_col
            year_col = candidates[0]
            print(f"⚠️  Inferred year column: '{year_col}' (was '{old}')")
        else:
            raise KeyError(f"Column '{year_col}' not found and no year-like column available.")
"""

if re.search(pattern, text):
    patched = re.sub(pattern, inference, text, count=1)
    file.write_text(patched, encoding="utf-8")
    print("✅ Patched plot_lcoe to auto-infer missing columns.")
else:
    print("❌ Failed to patch plot_lcoe: function signature not found.")