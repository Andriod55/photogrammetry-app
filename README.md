# photogrammetry-app

This project provides a simple 3D capture and viewer pipeline similar to Matterport. It consists of a Node.js/Express backend that orchestrates a Python photogrammetry pipeline and a React frontend for uploading image sets and viewing the resulting model.

## Quick Start

```bash
npm install
npm run start
```

The `start` script runs both the backend and frontend in development mode. The frontend proxy configuration forwards API requests to the backend.

## Project Structure

- `backend/` – Express server (`app.js`) and Python pipeline (`pipeline.py`).
- `frontend/` – React + Vite application with a simple uploader and 3D viewer.
- `docker-compose.yml` – Example services for running the frontend and backend in containers.

## Notes

The Python pipeline expects COLMAP, OpenMVS and Open3D to be installed in the execution environment. The provided code only demonstrates the command flow and does not include full error handling or production optimizations.

## Docker

Build and run the services with docker compose:

```bash
docker-compose up --build
```
