#!/usr/bin/env python3
"""
Script to create the recommended folder structure for
the Global Energy Transition Analysis repo.
"""

import os
from pathlib import Path

def create_dirs(dirs):
    for d in dirs:
        path = Path(d)
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {path}")

def create_gitkeep(files):
    for f in files:
        path = Path(f)
        if not path.exists():
            path.touch()
            print(f"Created placeholder file: {path}")

if __name__ == "__main__":
    # Directories to create
    directories = [
        "Notebooks",
        "docs",
        ".github/workflows",
        "executed",
        "data/raw",
        "data/processed",
    ]

    # Placeholder files to keep empty folders in git
    gitkeep_files = [
        "data/.gitkeep",
        "Notebooks/.gitkeep",
        "docs/.gitkeep",
    ]

    create_dirs(directories)
    create_gitkeep(gitkeep_files)

    print("Folder structure initialized successfully.")