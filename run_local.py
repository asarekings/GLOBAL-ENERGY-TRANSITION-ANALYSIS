#!/usr/bin/env python3
"""
Run the full energy‐analysis pipeline and serve the generated HTML reports
locally on http://localhost:8000
"""

import os
import subprocess
import threading
import webbrowser
import shutil
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

# -------------- Pipeline Steps --------------

def run_data_ingest():
    from energy_analysis.data_ingest import main as ingest_main
    print("▶️  Running data ingestion...")
    ingest_main()

def run_preprocessing():
    from energy_analysis.preprocessing import main as prep_main
    print("▶️  Running preprocessing...")
    prep_main()

def run_scenario_simulation():
    from energy_analysis.scenario import main as scen_main
    print("▶️  Running scenario simulation...")
    scen_main()

def run_notebooks():
    """
    Execute and convert each notebook in Notebooks/ to HTML in executed/,
    ensuring config.yaml is present beside the notebook during execution.
    """
    print("▶️  Executing and converting notebooks to HTML...")
    notebooks_dir = Path("Notebooks")
    out_dir = Path("executed")
    out_dir.mkdir(exist_ok=True)

    # Copy config.yaml into the Notebooks/ folder so notebooks can open it
    shutil.copy("config.yaml", notebooks_dir / "config.yaml")

    for nb_path in notebooks_dir.glob("*.ipynb"):
        cmd = [
            "jupyter", "nbconvert",
            "--to", "html",
            "--execute", str(nb_path),
            "--ExecutePreprocessor.timeout=600",
            "--output-dir", str(out_dir)
        ]
        print("   •", " ".join(cmd))
        subprocess.run(cmd, check=True)

def build_pipeline():
    run_data_ingest()
    run_preprocessing()
    run_scenario_simulation()
    run_notebooks()
    print("✅ Pipeline complete. HTML reports generated in ./executed")

# -------------- HTTP Server --------------

from pathlib import Path

class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # suppress console logs
        pass

def serve_reports(port=8000, directory="executed"):
    os.chdir(directory)
    handler = SilentHandler
    httpd = TCPServer(("", port), handler)
    url = f"http://localhost:{port}"
    print(f"🚀 Serving reports at {url}")
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server.")
    finally:
        httpd.server_close()

# -------------- Main Entrypoint --------------

if __name__ == "__main__":
    build_pipeline()
    # serve in a background thread so KeyboardInterrupt works
    server_thread = threading.Thread(
        target=serve_reports, 
        kwargs={"port":8000, "directory":"executed"},
        daemon=True
    )
    server_thread.start()
    server_thread.join()