"""
Grid operations and transformations
"""

import numpy as np
import open3d as o3d
from typing import List, Dict


class GridOperations:
    """
    Handles grid creation, serialization, and transformations
    """
    
    @staticmethod
    def serialize_line_sets(line_sets):
        """
        Serialize line sets to dictionary format for storage
        """
        data = []
        for i, ls in enumerate(line_sets):
            if not isinstance(ls, o3d.geometry.LineSet):
                raise TypeError(f"Element at index {i} is not a LineSet, but {type(ls)}")
            
            entry = {
                "points": np.asarray(ls.points),
                "lines": np.asarray(ls.lines),
                "colors": np.asarray(ls.colors),
            }
            data.append(entry)
        return data
    
    @staticmethod
    def deserialize_line_sets(grid_path):
        data = np.load(grid_path, allow_pickle=True)["data"]

        line_sets = []
        for entry in data:
            ls = o3d.geometry.LineSet()
            ls.points = o3d.utility.Vector3dVector(entry["points"])
            ls.lines = o3d.utility.Vector2iVector(entry["lines"])
            ls.colors = o3d.utility.Vector3dVector(entry["colors"])

            ls.translate((0, 0.0, -5))
            line_sets.append(ls)

        return line_sets

    @staticmethod
    def generate_grid(rects, h, resolution):
        """
        Create line sets from rectangle coordinates
        """
        line_sets = []
        for group in rects:
            for j, quad in enumerate(group):
                # Convert to meters
                color = [0, 1, 0]  # Green color
                quad = [[x * resolution, (h - y) * resolution] for x, y in quad]
                cube = GridOperations.create_cube_lines_from_quad(quad, height=15.0, color=color)
                line_sets.append(cube)

        return line_sets
    
    @staticmethod
    def line_sets_translation(line_sets, translation):
        """
        Apply translation to all line sets
        """
        for cube in line_sets:
            cube.translate(translation)
        return line_sets

    @staticmethod
    def rotate_grid(line_sets, rotation_matrix, rotation_center):
        """
        Apply rotation to all line sets
        """
        for cube in line_sets: 
            cube.rotate(rotation_matrix, center=rotation_center)
        return line_sets

    @staticmethod
    def create_cube_lines_from_quad(quad, height = 40.0, color = [0, 0, 0]):
        """
        Create a cube as line set from a 2D quadrilateral
        """
        quad = np.array(quad, dtype=np.float32)
        if quad.shape != (4, 2):
            raise ValueError("Quad must have exactly 4 points (x, y).")

        # Bottom (z=0) and top (z=height) faces
        bottom = np.hstack([quad, np.zeros((4, 1))])
        top = np.hstack([quad, np.full((4, 1), height)])
        points = np.vstack([bottom, top])  # Total: 8 points

        # Line indices for cube edges
        lines = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom face
            [4, 5], [5, 6], [6, 7], [7, 4],  # Top face
            [0, 4], [1, 5], [2, 6], [3, 7],  # Vertical edges
        ]

        # Assign color to all lines
        colors = [color for _ in lines]

        # Create LineSet
        line_set = o3d.geometry.LineSet()
        line_set.points = o3d.utility.Vector3dVector(points)
        line_set.lines = o3d.utility.Vector2iVector(lines)
        line_set.colors = o3d.utility.Vector3dVector(colors)

        return line_set
