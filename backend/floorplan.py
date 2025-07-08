"""Generate a simple SVG floor plan from detected planes."""
import argparse
import open3d as o3d


def generate_floorplan(mesh_path, svg_path):
    mesh = o3d.io.read_triangle_mesh(mesh_path)
    pcd = mesh.sample_points_uniformly(number_of_points=5000)
    # Placeholder plane segmentation
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,
                                             ransac_n=3,
                                             num_iterations=1000)
    inlier_cloud = pcd.select_by_index(inliers)
    bbox = inlier_cloud.get_axis_aligned_bounding_box()
    min_bound = bbox.min_bound
    max_bound = bbox.max_bound

    width, height = max_bound[0] - min_bound[0], max_bound[1] - min_bound[1]
    with open(svg_path, 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
        for pt in inlier_cloud.points:
            x, y, _ = pt
            f.write(f'<circle cx="{x - min_bound[0]}" cy="{y - min_bound[1]}" r="1" fill="black" />\n')
        f.write('</svg>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mesh', help='Path to mesh OBJ')
    parser.add_argument('svg', help='Output SVG path')
    args = parser.parse_args()
    generate_floorplan(args.mesh, args.svg)
