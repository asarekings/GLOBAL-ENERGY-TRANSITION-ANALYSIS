#!/usr/bin/env python3
"""
Patch the 04_levelized_cost_modeling notebook to avoid KeyError on missing columns.
Replaces the final DataFrame selection `df[['year','technology','capex']].head()`
with a simple `df.head()` so it always works.
"""
import nbformat
from pathlib import Path

nb_file = Path("Notebooks/04_levelized_cost_modeling.ipynb")
if not nb_file.exists():
    print("Notebook 04_levelized_cost_modeling.ipynb not found.")
    exit(1)

nb = nbformat.read(str(nb_file), as_version=4)
patched = False

for cell in nb.cells:
    if cell.cell_type == "code" and "plot_lcoe" in cell.source:
        # Build new source lines, dropping any df[['...']].head() lines
        lines = cell.source.splitlines()
        new_lines = []
        for ln in lines:
            if ln.strip().startswith("df[['") and ".head()" in ln:
                continue
            new_lines.append(ln)
        # Append a fallback display
        new_lines.append("df.head()")
        cell.source = "\n".join(new_lines)
        patched = True
        break

if patched:
    nbformat.write(nb, str(nb_file))
    print("Patched 04_levelized_cost_modeling.ipynb to use df.head().")
else:
    print("Did not find target cell to patch in 04_levelized_cost_modeling.ipynb.")