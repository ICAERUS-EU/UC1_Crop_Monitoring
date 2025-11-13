import os 
import numpy as np
import open3d as o3d
from pointcloud.pointcloud_loader import PointCloudLoader

class PointCloudDownsampler:
    def __init__(self, config, base_dir):
        self.config = config
        self._base_dir = base_dir
        self._years = ["2023", "2024"]        

    def process_downsample(self):
        print("Starting pointcloud downsampling...")

        for year in self._years:
            zenodo_base_year = os.path.join(self.config['io']['zenodo_base_dir'], year)
            
            if not os.path.exists(zenodo_base_year):
                print(f"Year directory not found: {zenodo_base_year}")
                continue
            
            print(f"\nProcessing year: {year}")
            dates = sorted([d for d in os.listdir(zenodo_base_year) 
                          if os.path.isdir(os.path.join(zenodo_base_year, d))])
            
            for date in dates:
                if date == '230505':
                    continue
                print(f"Processing {year}/{date}")
                filename = PointCloudLoader._get_pointcloud_path(self.config, year, date)
                print("  input path:", filename)
                cloud = PointCloudLoader.load_cloud(filename)
                cloud = self._filter_outliers_cloud(cloud)
                cloud = self._downsample_cloud(cloud, self.config["data_sources"]["voxel_size"], False)
                if cloud is not None:
                    self._save_downsampled_cloud(cloud, year, date)
        print("\nGrid computation completed!")

    def _filter_outliers_cloud(self, cloud):
        cloud_out, _ = cloud.remove_statistical_outlier(nb_neighbors=30, std_ratio=2.5) 
        return cloud_out

    def _downsample_cloud(self, cloud, voxel_size = 0.05, visualize = False):
        """
        Downsample a point cloud using a voxel grid.
        """
        if not isinstance(cloud, o3d.geometry.PointCloud):
            raise TypeError("Input must be an open3d.geometry.PointCloud object.")

        if voxel_size <= 0:
            raise ValueError("Voxel size must be positive.")

        print(f"  Downsampling cloud with voxel size = {voxel_size:.3f}")
        cloud_down = cloud.voxel_down_sample(voxel_size=voxel_size)

        if visualize:
            print("  Visualizing original and downsampled clouds...")
            o3d.visualization.draw_geometries([cloud, cloud_down])

        print(f"  Downsampled from {len(cloud.points)} →  {len(cloud_down.points)} points")
        return cloud_down
    
    def _save_downsampled_cloud(self, cloud, year, date):
        """Save processed grid data to file"""
        out_suffix = self.config["data_sources"]["out_suffix"]["rgb"]
        output_dir = os.path.join(self._base_dir, self.config["io"]["downsample_dir"].format(suffix=out_suffix), year)
        
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"vineyard_{date}{out_suffix}.txt")

        p = np.asarray(cloud.points)
        c = (np.asarray(cloud.colors) * 255).astype(int)  # Denormalize
        n = np.asarray(cloud.normals)
        data = np.hstack((p, c, n))
        np.savetxt(output_path, data, fmt="%.3f %.3f %.3f %d %d %d %.6f %.6f %.6f")
        print(f"  Saved downsampled cloud to: {output_path}\n")

