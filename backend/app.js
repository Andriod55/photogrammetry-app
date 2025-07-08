const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(express.json());

app.post('/api/upload', upload.single('images'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const inputZip = req.file.path;
  const tempDir = fs.mkdtempSync(path.join('uploads', 'set-'));
  const outputDir = path.join(tempDir, 'output');
  fs.mkdirSync(outputDir, { recursive: true });

  // Unzip images
  const unzip = spawn('unzip', [inputZip, '-d', tempDir]);
  unzip.on('exit', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: 'Failed to unzip images' });
    }

    const py = spawn('python3', ['backend/pipeline.py', tempDir, outputDir]);
    py.stdout.on('data', (data) => console.log(data.toString()));
    py.stderr.on('data', (data) => console.error(data.toString()));

    py.on('close', (code) => {
      fs.unlinkSync(inputZip);
      if (code !== 0) {
        return res.status(500).json({ error: 'Pipeline failed' });
      }
      res.json({ message: 'Processing complete', output: outputDir });
      // NOTE: In production, you would serve files or save metadata to DB.
    });
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Backend listening on ${PORT}`));
