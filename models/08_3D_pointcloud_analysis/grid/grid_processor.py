"""
Main grid processor for 3D grid computation
"""

import os
import sys
import json
import numpy as np
import open3d as o3d

from orthomosaic.orthomosaic_loader import OrthomosaicLoader
from pointcloud.pointcloud_loader import PointCloudLoader
from grid.grid_operations import GridOperations
from grid.grid_alignment import GridAlignment


class GridProcessor:
    """Main class for processing grid data across multiple years and dates"""
    
    def __init__(self, config, base_dir):
        self.config = config
        self._base_dir = base_dir
        self._resolution = 0.038
        self._image_height = 3610  
        self.years = ['2023', '2024']
        self._root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self._data_dir = os.path.join(self._root, '08_3D_pointcloud_analysis/data')
        self.rects = self._load_parcel_points()        
        ndvi = config.get("ndvi", False)
        self.suffix = ''
        if ndvi: 
            self.suffix = '_NDVI'

    def _load_parcel_points(self):
        """Load parcel points from JSON file"""
        parcel_points_path = os.path.join(self._data_dir, self.config['data_sources']['parcel_points_file'])
        try:
            with open(parcel_points_path, "r") as f:
                return json.load(f)
        except:
            print(f"Error: Parcel points file could not be loaded: {parcel_points_path}")
            sys.exit(1)
        
    def _get_orthomosaic_path(self, year, date):
        """Get orthomosaic file path for given year and date"""
        path_template = self.config['paths']['orthomosaic']
        return path_template.format(
            zenodo_base=self.config['io']['zenodo_base_dir'],
            year=year,
            date=date
        )
    
    def _process_date(self, year, date):
        """
        Process data for a specific date
        Returns serialized line sets data if successful, None otherwise
        """        
        # Construct file paths
        pointcloud_path = PointCloudLoader._get_pointcloud_path(self.config, year, date, self.suffix)
        orthomosaic_path = self._get_orthomosaic_path(year, date)
        
        # Load point cloud
        print("  Loading point cloud...")
        cloud1 = PointCloudLoader.load_cloud(pointcloud_path)

        # Load orthomosaic image
        print("  Loading orthomosaic...")
        img_rgb = OrthomosaicLoader.load_orthomosaic(orthomosaic_path)
        
        # Create color orthomosaic plane and orient cloud
        print("  Creating color plane...")
        cloud2 = OrthomosaicLoader.create_color_plane_from_image(img_rgb, self._resolution)
        cloud2, rotation_matrix, rotation_center = PointCloudLoader.orient_cloud(cloud1, cloud2)
        
        # Extract green points and create line sets (grid)
        print("  Extracting green points...")
        green_points_array, green_pcd = PointCloudLoader.extract_green_cloud(cloud1)

        # Generate grid from parcel points
        print("  Generating grid...")
        line_sets = GridOperations.generate_grid(self.rects, self._image_height, self._resolution)
        line_sets = GridOperations.rotate_grid(line_sets, rotation_matrix, rotation_center)
        
        # Align point clouds and line sets (grid)
        print("  Aligning point clouds...")
        cloud2, translation = GridAlignment.align_pointcloud_with_corner(cloud1, cloud2)
        line_sets = GridOperations.line_sets_translation(line_sets, translation)
        
        # Optimize alignment, look for best translation
        print("  Optimizing grid position...")
        line_sets, best_translation = GridAlignment.perform_best_translation(line_sets, green_pcd)
        
        # Visualize results
        o3d.visualization.draw_geometries([cloud1, cloud2] + line_sets)
        
        # Serialize and return data
        return GridOperations.serialize_line_sets(line_sets)
    
    def _save_results(self, data, year, date):
        """Save processed grid data to file"""
        output_dir = os.path.join(self._base_dir, f"data/grids{self.suffix}/{year}")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f"grid_{date}{self.suffix}.npz")
        np.savez(output_path, data=data)
        print(f"  Saved grid data to: {output_path}\n")
    
    def compute_grid(self):
        """Main processing loop for all years and dates"""
        print("Starting grid computation...")
        
        for year in self.years:
            zenodo_base_year = os.path.join(self.config['io']['zenodo_base_dir'], year)
            
            if not os.path.exists(zenodo_base_year):
                print(f"Year directory not found: {zenodo_base_year}")
                continue
            
            print(f"\nProcessing year: {year}")
            dates = sorted([d for d in os.listdir(zenodo_base_year) 
                          if os.path.isdir(os.path.join(zenodo_base_year, d))])
            
            for date in dates:
                print(f"Processing {year}/{date}")
                result = self._process_date(year, date)
                if result is not None:
                    self._save_results(result, year, date)
        
        print("\nGrid computation completed!")