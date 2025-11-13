import os
import numpy as np 
import open3d as o3d

class PointCloudGroundPlant:

    @staticmethod
    def extract_ground_by_grid_min(cloud, cell_size=0.27, height_tol=0.29, show=True):
        """
        Extracts ground points by:
        1. Dividing the cloud into XY grid cells.
        2. Finding the lowest Z in each cell.
        3. Including all points within `height_tol` above that minimum.
        """
        points = np.asarray(cloud.points)
        colors = np.asarray(cloud.colors)

        # Assign cell keys (integer grid coordinates)
        cell_keys = np.floor(points[:, :2] / cell_size).astype(np.int32)

        # Encode keys into a single integer for grouping
        # (safe if grid index fits in int64)
        key_hash = cell_keys[:, 0].astype(np.int64) << 32 | (cell_keys[:, 1] & 0xffffffff)

        # Step 1: Find min Z per cell
        unique_keys, inverse_idx = np.unique(key_hash, return_inverse=True)
        min_z_per_cell = np.zeros(len(unique_keys), dtype=np.float32)
        min_z_per_cell.fill(np.inf)
        np.minimum.at(min_z_per_cell, inverse_idx, points[:, 2])

        # Step 2: Select points within tolerance
        mask = points[:, 2] <= min_z_per_cell[inverse_idx] + height_tol

        # Create result cloud
        ground_cloud = o3d.geometry.PointCloud()
        ground_cloud.points = o3d.utility.Vector3dVector(points[mask])
        ground_cloud.colors = o3d.utility.Vector3dVector(colors[mask])

        return ground_cloud


    @staticmethod
    def subtract_clouds(original_cloud, ground_cloud, tol=1e-6):
        """
        Subtract ground_cloud from original_cloud (optimized).
        Returns a point cloud with only non-ground points.
        """
        # Extract as float32 for memory efficiency
        orig_points = np.asarray(original_cloud.points, dtype=np.float32)
        orig_colors = np.asarray(original_cloud.colors, dtype=np.float32)
        ground_points = np.asarray(ground_cloud.points, dtype=np.float32)

        # Scale & quantize
        scale = 1.0 / tol
        orig_quant = np.round(orig_points * scale).astype(np.int64)
        ground_quant = np.round(ground_points * scale).astype(np.int64)

        # Structured array view (treat each point as a single record)
        orig_struct = orig_quant.view([('', np.int64)] * 3).reshape(-1)
        ground_struct = ground_quant.view([('', np.int64)] * 3).reshape(-1)

        # Fast set-like operation: keep only points not in ground
        mask = ~np.isin(orig_struct, ground_struct)

        # Apply mask
        non_ground_cloud = o3d.geometry.PointCloud()
        non_ground_cloud.points = o3d.utility.Vector3dVector(orig_points[mask])
        non_ground_cloud.colors = o3d.utility.Vector3dVector(orig_colors[mask])

        return non_ground_cloud
    
    @staticmethod
    def save_cloud(base_dir, date, year, suffix, cloud, plant=True): 

        directory = f"{base_dir}/data/plant_clouds{suffix}" if plant else f"{base_dir}/data/ground_clouds{suffix}"
        filename = f"plant_cloud_{date}{suffix}.ply" if plant else f"ground_cloud_{date}{suffix}.ply"

        print(directory)
        os.makedirs(directory, exist_ok=True)
        o3d.io.write_point_cloud(f"{directory}/{year}/{filename}", cloud)
        print(f"[INFO] Saved cloud in {directory}/{year}/{filename}")
