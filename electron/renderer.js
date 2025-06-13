const form = document.getElementById('upload');
const output = document.getElementById('output');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = document.getElementById('pano').files[0];
  if (!file) return;
  const data = new FormData();
  data.append('file', file);

  // Save file locally and call backend
  const fs = require('fs');
  const path = require('path');
  const tmpPath = path.join(__dirname, file.name);
  fs.writeFileSync(tmpPath, Buffer.from(await file.arrayBuffer()));

  const res = await fetch('http://localhost:5000/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pano_path: tmpPath }),
  });
  const json = await res.json();
  output.innerText = JSON.stringify(json, null, 2);
});
