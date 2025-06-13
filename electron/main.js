const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

function createWindow() {
  // Spawn backend API
  const backend = spawn('python', [path.join(__dirname, '../backend/api.py')]);
  backend.stdout.on('data', data => console.log(`[backend] ${data}`));
  backend.stderr.on('data', data => console.error(`[backend] ${data}`));

  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadFile('renderer.html');
}

app.whenReady().then(createWindow);
