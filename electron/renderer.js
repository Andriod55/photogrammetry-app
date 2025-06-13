const form = document.getElementById('upload');
const output = document.getElementById('output');
const viewer = document.getElementById('viewer');

const THREE = require('three');
const { PLYLoader } = require('three/examples/jsm/loaders/PLYLoader.js');
let scene, camera, renderer;

function initThree() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, viewer.clientWidth / viewer.clientHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer();
  renderer.setSize(viewer.clientWidth, viewer.clientHeight);
  viewer.appendChild(renderer.domElement);
  camera.position.z = 2;
  animate();
}

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

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

  const loader = new PLYLoader();
  loader.load(`http://localhost:5000/workspace/${file.name}/gsplat/point_cloud.ply`, ply => {
    ply.computeVertexNormals();
    scene.add(new THREE.Mesh(ply, new THREE.MeshStandardMaterial({ color: 0xcccccc })));
  });
});

initThree();
