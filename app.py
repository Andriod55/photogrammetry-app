# File: photogrammetry-app/backend/app.py
"""
Backend Python script for the 360° Photogrammetry App.
This script performs:
1. Conversion of an equirectangular panorama to cubemap faces.
2. Execution of COLMAP for reconstruction (SfM/MVS).
3. (Pseudo-code) 3D Gaussian Splatting using gsplat.

Before running, ensure that the dependencies listed in requirements.txt are installed.
"""

import os
import subprocess
from PIL import Image
from py360convert import e2c

def convert_equirect_to_cubemap(input_image_path, output_dir, face_width):
    """
    Convert an equirectangular image to a cubemap.
    Saves six face images (front, right, back, left, up, down) in the output directory.
    """
    print("Starting cubemap conversion...")
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(input_image_path)
    # e2c returns a list of six PIL images
    faces = e2c(img, face_w=face_width)

    face_names = ["front", "right", "back", "left", "up", "down"]
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]

    for name, face_img in zip(face_names, faces):
        out_path = os.path.join(output_dir, f"{base_name}_{name}.jpg")
        face_img.save(out_path)
        print(f"Saved: {out_path}")

    print("Cubemap conversion completed.")

def run_colmap_automatic_reconstructor(image_dir, workspace_dir, quality="medium"):
    """
    Run COLMAP's automatic reconstructor on the provided images.
    Make sure COLMAP is installed and accessible in your PATH.
    """
    print("Starting COLMAP automatic reconstruction...")
    cmd = [
        "colmap", "automatic_reconstructor",
        "--image_path", image_dir,
        "--workspace_path", workspace_dir,
        "--quality", quality
    ]
    try:
        subprocess.run(cmd, check=True)
        print("COLMAP reconstruction completed.")
    except subprocess.CalledProcessError as e:
        print("COLMAP reconstruction failed:", e)

def run_gsplat(colmap_output_path, gsplat_output_path):
    """
    (Pseudo-code) Run 3D Gaussian Splatting using gsplat.
    Replace with the actual gsplat API calls if available.
    """
    print("Starting 3D Gaussian Splatting (this is pseudo-code)...")
    try:
        import gsplat  # Ensure gsplat is installed if you want to use it.
        # Pseudo-code: load COLMAP data, optimize the Gaussian splat model, and export it.
        model = gsplat.load_from_colmap(colmap_output_path)
        model.optimize(iterations=1000)
        model.export(gsplat_output_path)
        print("3D Gaussian Splatting completed.")
    except ImportError:
        print("gsplat not installed. Skipping 3D Gaussian Splatting.")
    except Exception as e:
        print("Error during 3D Gaussian Splatting:", e)

if __name__ == '__main__':
    # Define file and directory paths (adjust as needed)
    input_image = os.path.join("assets", "panorama1.jpg")
    cubemap_dir = os.path.join("assets", "cubemaps")
    colmap_workspace = os.path.join("assets", "colmap_workspace")
    gsplat_output = os.path.join("assets", "gsplat_model.spz")

    # Step 1: Convert the panorama to cubemap faces.
    convert_equirect_to_cubemap(input_image, cubemap_dir, face_width=2048)

    # Step 2: Run COLMAP reconstruction using the cubemap images.
    run_colmap_automatic_reconstructor(cubemap_dir, colmap_workspace, quality="medium")

    # Step 3: Process COLMAP outputs with 3D Gaussian Splatting (psuedo-code).
    run_gsplat(colmap_workspace, gsplat_output)

    print("Backend processing completed. Exiting.")