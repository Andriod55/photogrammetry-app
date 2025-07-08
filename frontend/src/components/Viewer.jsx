import React, { useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

export default function Viewer({ outputDir }) {
  // Placeholder viewer: In a real app, fetch PLY/OBJ files from server
  return (
    <div style={{ height: '500px' }}>
      <Canvas>
        <OrbitControls />
        <ambientLight />
        <pointLight position={[10, 10, 10]} />
        {/* Load and display geometry here */}
      </Canvas>
    </div>
  );
}
