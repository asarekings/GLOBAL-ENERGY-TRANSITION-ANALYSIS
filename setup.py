from setuptools import setup, find_packages

setup(
    name="energy_analysis",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "pandas", "numpy", "matplotlib", "seaborn",
        "scikit-learn", "pyyaml", "nbconvert",
        "statsmodels", "plotly", "requests"
    ],
    python_requires=">=3.8",
)
