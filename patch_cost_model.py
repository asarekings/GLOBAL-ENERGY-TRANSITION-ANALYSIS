#!/usr/bin/env python3
"""
Patch cost_model.py to use seaborn theme instead of invalid matplotlib style.
"""

from pathlib import Path
import re

file = Path("src/energy_analysis/analysis/cost_model.py")
if not file.exists():
    print("cost_model.py not found, skipping patch.")
    exit(1)

content = file.read_text(encoding="utf-8")
# Ensure seaborn is imported
if "import seaborn as sns" not in content:
    content = content.replace(
        "import matplotlib.pyplot as plt",
        "import matplotlib.pyplot as plt\nimport seaborn as sns"
    )

# Replace any plt.style.use(...) for seaborn-darkgrid with sns.set_theme(...)
content = re.sub(
    r"plt\.style\.use\([\"'].*seaborn-darkgrid.*[\"']\)",
    "sns.set_theme(style='darkgrid')",
    content
)

file.write_text(content, encoding="utf-8")
print("Patched cost_model.py with seaborn theme.")