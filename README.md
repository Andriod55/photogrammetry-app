# Photogrammetry App

This repository contains a minimal skeleton for a desktop photogrammetry
application using Python and Electron.

## Setup

Run `bash install.sh` to create a Python virtual environment, install
backend requirements and install the Electron dependencies.

Start the application with:

```bash
npm start
```

The Electron frontend spawns a Flask server exposing a `/process`
endpoint that runs the photogrammetry pipeline defined in
`backend/core.py`.
