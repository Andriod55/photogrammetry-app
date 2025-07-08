import React, { useState } from 'react';
import Viewer from './components/Viewer';

export default function App() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState('Idle');
  const [outputDir, setOutputDir] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    const data = new FormData();
    data.append('images', file);
    setProgress('Uploading...');
    const res = await fetch('/api/upload', {
      method: 'POST',
      body: data,
    });
    if (!res.ok) {
      setProgress('Error during upload');
      return;
    }
    const json = await res.json();
    setOutputDir(json.output);
    setProgress('Complete');
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Photogrammetry App</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".zip" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit">Upload</button>
      </form>
      <p>Progress: {progress}</p>
      {outputDir && <Viewer outputDir={outputDir} />}
    </div>
  );
}
