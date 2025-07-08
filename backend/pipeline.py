import argparse
import logging
import os
import shutil
import subprocess
import tempfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def run_cmd(cmd, cwd=None):
    logging.info('Running: %s', ' '.join(cmd))
    try:
        subprocess.run(cmd, cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        logging.error('Command failed: %s', e)
        raise


def run_pipeline(images_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    sparse_dir = os.path.join(output_dir, 'sparse')
    dense_dir = os.path.join(output_dir, 'dense')
    mesh_dir = os.path.join(output_dir, 'mesh')
    os.makedirs(sparse_dir, exist_ok=True)
    os.makedirs(dense_dir, exist_ok=True)
    os.makedirs(mesh_dir, exist_ok=True)

    # 1. COLMAP feature extraction and sparse reconstruction
    run_cmd(['colmap', 'automatic_reconstructor',
             '--image_path', images_dir,
             '--workspace_path', output_dir,
             '--workspace_format', 'COLMAP',
             '--data_type', 'image',
             '--use_gpu', '1'])

    # 2. Convert COLMAP result to OpenMVS format
    run_cmd(['InterfaceCOLMAP',
             '--input_path', os.path.join(output_dir, 'sparse/0'),
             '--output_path', os.path.join(output_dir, 'scene.mvs')])

    # 3. OpenMVS dense reconstruction
    run_cmd(['DensifyPointCloud', os.path.join(output_dir, 'scene.mvs'),
             '--resolution-level', '1'])
    run_cmd(['ReconstructMesh', os.path.join(output_dir, 'scene_dense.mvs')])
    run_cmd(['TextureMesh', os.path.join(output_dir, 'scene_dense_mesh.mvs')])

    # 4. Open3D post-processing (placeholder)
    # In a real setup, call Open3D for cleanup and plane extraction.
    # Example: python -m open3d.utility.pointcloud --input <file> --output <file>

    logging.info('Pipeline completed. Results stored in %s', output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Photogrammetry pipeline')
    parser.add_argument('images', help='Path to images directory')
    parser.add_argument('output', help='Path to output directory')
    args = parser.parse_args()

    run_pipeline(args.images, args.output)
