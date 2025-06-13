"""Flask API exposing the photogrammetry pipeline."""

from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

import core

app = Flask(__name__)


@app.post("/process")
def process() -> tuple[str, int]:
    """Process an uploaded panorama."""
    data = request.get_json(force=True)
    pano_path = data["pano_path"]
    workspace = data.get("workspace", "workspace")
    out_dir = core.run_pipeline(pano_path, workspace)
    return jsonify({"output": str(out_dir)})


@app.get("/workspace/<path:filename>")
def workspace_file(filename: str):
    """Serve files from the workspace directory."""
    return send_from_directory("workspace", filename)


if __name__ == "__main__":
    app.run(port=5000)
