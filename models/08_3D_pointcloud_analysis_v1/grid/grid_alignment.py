"""
Grid alignment and optimization utilities
"""

import numpy as np
import open3d as o3d
from tqdm import tqdm
from typing import List, Tuple
from grid.grid_operations import GridOperations


class GridAlignment:
    """
    Handles grid alignment and optimization operations
    """
    
    @staticmethod
    def get_upper_left(cloud):
        """
        Get upper left corner point of point cloud
        """
        pts = np.asarray(cloud.points)
        min_x = np.min(pts[:, 0])
        max_y = np.max(pts[:, 1])
        min_z = np.min(pts[:, 2])  

        return np.array([min_x, max_y, min_z])

    @staticmethod
    def align_pointcloud_with_corner(cloud1, cloud2):
        """
        Align two point clouds by their upper left corners
        """
        origin1 = GridAlignment.get_upper_left(cloud1)
        origin2 = GridAlignment.get_upper_left(cloud2)

        delta = origin1 - origin2
        delta[-1] = delta[-1] - 2.5  # Z offset adjustment
        cloud2.translate(delta)

        return cloud2, delta

    @staticmethod
    def get_top_right_point(green_points_array):
        """
        Find top-right point from green points array
        """
        # Sort by Y descending
        sorted_by_y = green_points_array[np.argsort(-green_points_array[:, 1])]

        # Take top N points by Y
        N = 5
        top_N = sorted_by_y[:N]

        # Find rightmost point among top points
        min_x_idx = np.argmax(top_N[:, 0])
        top_right_point = top_N[min_x_idx]

        return top_right_point

    @staticmethod
    def align_line_sets_with_point(line_sets, top_right_point):
        """
        Align line sets to a reference point
        """
        reference_cube = line_sets[13]
        cube_points = np.asarray(reference_cube.points)

        # Find top-right point in cube
        idx_top_right = np.argmax(cube_points[:, 0] + cube_points[:, 1])
        cube_top_right_point = cube_points[idx_top_right]
        translation_vector = top_right_point - cube_top_right_point

        # Apply translation
        line_sets = GridOperations.line_sets_translation(line_sets, translation_vector)
        
        return line_sets

    @staticmethod
    def is_point_in_bbox(point, bbox_min, bbox_max):
        """
        Check if point is inside bounding box
        
        Args:
            point: Point coordinates
            bbox_min: Bounding box minimum coordinates
            bbox_max: Bounding box maximum coordinates
            
        Returns:
            bool: True if point is inside bbox
        """
        return np.all(point >= bbox_min) and np.all(point <= bbox_max)

    @staticmethod
    def perform_best_translation(line_sets, green_pcd, visualize = False):
        """
        Find optimal translation for line sets to maximize green points inside
        """
        dx_range = np.linspace(-1.0, 1.0, 11)
        dy_range = np.linspace(-1.0, 1.0, 11)

        best_translation = np.array([0.0, 0.0, 0.0])
        best_count = -1

        for dx in tqdm(dx_range, desc="Optimizing translation"):
            for dy in dy_range:
                offset = np.array([dx, dy, 0.0])
                total = 0
                visual_objs = []

                for cube in line_sets:
                    cube.translate(offset)
                    bbox = o3d.geometry.OrientedBoundingBox.create_from_points(
                        o3d.utility.Vector3dVector(cube.points)
                    )
                    inside_pcd = green_pcd.crop(bbox)

                    if len(inside_pcd.points) > 0:
                        inside_points = np.asarray(inside_pcd.points)
                        total += len(inside_points)

                        if visualize:
                            bbox.color = (1, 0, 1)  # Magenta
                            inside_pcd.paint_uniform_color([0, 1, 0])  # Green
                            visual_objs.append(inside_pcd)
                            visual_objs.append(bbox)

                    cube.translate(-offset)

                if visualize and total > 0:
                    o3d.visualization.draw_geometries(visual_objs)
                    
                print(f"dx={dx:.2f}, dy={dy:.2f} ➤ points inside: {total}")

                if total > best_count:
                    best_count = total
                    best_translation = offset.copy()

        print(f"Best translation: {best_translation} with {best_count} points inside")
        line_sets = GridOperations.line_sets_translation(line_sets, best_translation)

        return line_sets, best_translation

