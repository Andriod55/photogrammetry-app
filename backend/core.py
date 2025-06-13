"""Core photogrammetry pipeline functions."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

import cv2
import py360convert

try:
    import gsplat.simple_trainer as gst
except ImportError:  # gsplat is optional
    gst = None


def equirectangular_to_cubemap(pano_path: str, out_dir: str) -> list[Path]:
    """Convert an equirectangular panorama to cubemap faces.

    Parameters
    ----------
    pano_path:
        Path to the equirectangular panorama image.
    out_dir:
        Directory where the cubemap faces will be saved.

    Returns
    -------
    list[Path]
        Paths to the generated cubemap face images.
    """
    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)
    img = cv2.imread(pano_path)
    faces = []
    for face_idx in range(6):
        face = py360convert.e2c(img, face_idx=face_idx, cube_format="dice")
        face_path = out_dir_path / f"face_{face_idx}.jpg"
        cv2.imwrite(str(face_path), face)
        faces.append(face_path)
    return faces


def run_colmap(img_dir: str, workspace_dir: str, quality: str = "medium") -> None:
    """Run COLMAP's automatic reconstructor on a directory of images."""
    subprocess.run(
        [
            "colmap",
            "automatic_reconstructor",
            "--image_path",
            img_dir,
            "--workspace_path",
            workspace_dir,
            "--quality",
            quality,
        ],
        check=True,
    )


def run_gsplat(dense_dir: str, out_dir: str) -> None:
    """Run Gaussian Splatting on the dense COLMAP output."""
    if gst is None:
        raise RuntimeError("gsplat is not installed")
    gst.main(["--data_dir", dense_dir, "--result_dir", out_dir])


def run_pipeline(pano_path: str, workspace_dir: str) -> Path:
    """Execute full pipeline from panorama to Gaussian Splatting output."""
    workspace = Path(workspace_dir)
    cubemap_dir = workspace / "cubemap"
    equirectangular_to_cubemap(pano_path, str(cubemap_dir))
    colmap_workspace = workspace / "colmap"
    run_colmap(str(cubemap_dir), str(colmap_workspace))
    gsplat_out = workspace / "gsplat"
    run_gsplat(str(colmap_workspace / "dense"), str(gsplat_out))
    return gsplat_out
