# Photogrammetry App

This repository provides a simple desktop application that demonstrates a 
photogrammetry workflow built with Python and Electron.

The backend converts a panorama to a cubemap, runs COLMAP to reconstruct a
scene and then launches Gaussian Splatting.  The Electron frontend allows you to
upload a panorama and visualize the pipeline output.

## Setup

Create a Python virtual environment and install dependencies along with the
Electron packages:

```bash
bash install.sh
```

Run the application with:

```bash
npm start
```

The Flask server exposes a `/process` endpoint used by the frontend.  It expects
JSON with `pano_path` pointing to the panorama image.  Results are written to the
`workspace/` directory relative to the repository root.

Once processing finishes you can browse the generated files via
`http://localhost:5000/workspace/...` in the browser.
