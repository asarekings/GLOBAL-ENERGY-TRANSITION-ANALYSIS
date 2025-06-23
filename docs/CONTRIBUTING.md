# Contributing Guide

## Setup

1. Fork and clone.
2. Create Conda env: `conda env create -f environment.yml`.
3. Activate: `conda activate energy-analysis`.
4. Install deps: `pip install -r requirements.txt`.
5. Run `make data preprocess notebooks` to verify.

## Workflow

- Add data sources in `config.yaml`.
- Update modules under `src/energy_analysis/`.
- Update notebooks.
- Ensure CI passes.

## Style

- PEP8 for code.
- Markdown narrative in notebooks.
