// File: photogrammetry-app/electron/main.js
// This is the Main process: it creates the app window and starts the Python backend.

const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pyProc;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,   // Using contextIsolation/separated environment for security.
      contextIsolation: true
    }
  });
  // Load the HTML file for the 3D viewer.
  mainWindow.loadFile(path.join(__dirname, "renderer", "index.html"));
}

function startPythonBackend() {
  // Path to the Python backend script.
  let script = path.join(__dirname, "..", "backend", "app.py");

  // Launch the Python process. Adjust "python" if your system requires "python3" or a full path.
  pyProc = spawn("python", [script]);

  pyProc.stdout.on("data", (data) => {
      console.log(`PYTHON: ${data}`);
      // Optionally, you can send these events to the renderer via IPC.
  });

  pyProc.stderr.on("data", (data) => {
      console.error(`PYTHON ERROR: ${data}`);
  });

  pyProc.on("close", (code) => {
      console.log(`Python backend exited with code ${code}`);
  });
}

app.whenReady().then(() => {
  createWindow();
  startPythonBackend();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  // Make sure to terminate the Python process on exit.
  if (pyProc) pyProc.kill();
  if (process.platform !== "darwin") app.quit();
});