// File: photogrammetry-app/electron/preload.js
// This preload script exposes a limited API for the renderer process.

const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  sendMessage: (msg) => ipcRenderer.send("message", msg),
  onMessage: (callback) => ipcRenderer.on("message", callback)
});