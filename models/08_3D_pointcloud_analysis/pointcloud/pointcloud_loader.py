"""
Point cloud loading and processing utilities
"""
import sys
import numpy as np
import open3d as o3d
from utils.utils import rotation_matrix_from_vectors


class PointCloudLoader:
    """
    Handles loading and basic processing of point cloud data
    """

    @staticmethod
    def _get_pointcloud_path(config, year, date, suffix):
        """Get pointcloud file path for given year and date"""
        path_template = config['paths']['pointcloud']
        return path_template.format(
            zenodo_base=config['io']['zenodo_base_dir'],
            year=year,
            date=date,
            suffix=suffix
        )
    
    @staticmethod
    def load_cloud(filename):
        """
        Load point cloud from text file with format: x y z r g b nx ny nz
        """
        try:
            data = np.loadtxt(filename)
            cloud = o3d.geometry.PointCloud()
            cloud.points = o3d.utility.Vector3dVector(data[:, :3])
            cloud.colors = o3d.utility.Vector3dVector(data[:, 3:6] / 255.0)            
            cloud.normals = o3d.utility.Vector3dVector(data[:, 6:9])
            return cloud
        except Exception as e:
            print(f"❌ Failed to load point cloud: {filename}")
            print(f"   Error: {e}")
            sys.exit(1)

    @staticmethod
    def orient_cloud(reference_cloud, cloud_to_align):
        """
        Align a point cloud to the orientation of a reference cloud's plane
        """
        # Calculate rotation center
        rotation_center = cloud_to_align.get_center()
        
        # Calculate reference plane normal using PCA
        pts = np.asarray(reference_cloud.points)
        centroid = np.mean(pts, axis=0)
        pts_centered = pts - centroid
        cov = np.cov(pts_centered.T)
        eigvals, eigvecs = np.linalg.eigh(cov)
        normal_vector = eigvecs[:, 0]  # Normal vector to the plane
        
        # Calculate and apply rotation
        R = rotation_matrix_from_vectors(np.array([0, 0, 1]), normal_vector)
        cloud_to_align.rotate(R, center=rotation_center)

        return cloud_to_align, R, rotation_center

    @staticmethod
    def extract_green_cloud(cloud):
        """
        Extract green points from point cloud using color thresholds
        """
        points = np.asarray(cloud.points)
        colors = np.asarray(cloud.colors)

        # Extract RGB channels
        r, g, b = colors[:, 0], colors[:, 1], colors[:, 2]

        # Threshold for "green" color
        green_mask = (g > 0.15) & (g > r + 0.01) & (g > b + 0.01)

        # Apply mask
        green_points_array = points[green_mask]
        green_colors_array = colors[green_mask]

        # Create point cloud
        green_pcd = o3d.geometry.PointCloud()
        green_pcd.points = o3d.utility.Vector3dVector(green_points_array)
        green_pcd.colors = o3d.utility.Vector3dVector(green_colors_array)
        
        print(f"  Total green points = {len(green_points_array)}")

        return green_points_array, green_pcd
       
