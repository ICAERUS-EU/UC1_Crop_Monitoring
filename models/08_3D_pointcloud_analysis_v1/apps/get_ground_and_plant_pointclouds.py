import os
import sys
import time
import numpy as np 
import open3d as o3d
from tqdm import tqdm

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pointcloud.pointcloud_loader import PointCloudLoader
from pointcloud.pointcloud_ground_plants import PointCloudGroundPlant
from grid.grid_operations import GridOperations
from utils.utils import load_config


def get_ground_and_plant_pointclouds(config, base_dir):
    io_cfg = config["io"]
    paths_cfg = config["paths"]
    down = config.get("downsample", True)
    dates = config.get("dates", [])
    suffix = "_down" if down else ""

    for date in tqdm(dates): 
        year = "20"+date[0:2]

        # Paths
        if down:
            cloud_path = os.path.join(base_dir, io_cfg["downsample_dir"].format(suffix=suffix), f"{year}/vineyard_{date}{suffix}.txt")
            plant_path = os.path.join(base_dir, io_cfg["plant_cloud_dir_down"], f"{year}/plant_cloud_{date}{suffix}.ply")

        else:
            cloud_path = os.path.join(io_cfg["zenodo_base_dir"], year, date, "POINTCLOUDS", f"CROPPED_POINTCLOUD_{date}.txt")
            plant_path = paths_cfg["plant_cloud"].format(plant_dir=io_cfg["plant_cloud_dir"], year=year, date=date, suffix=suffix)

        print(cloud_path)
        print(plant_path)
        if not os.path.exists(cloud_path) or not os.path.exists(plant_path):
            print(f"[SKIP] Missing cloud file for {date}")
            continue

        # Load cloud
        cloud = PointCloudLoader.load_cloud(cloud_path)
        plant_cloud = o3d.io.read_point_cloud(plant_path)

        # Load grid
        grid_path = os.path.join(base_dir, paths_cfg['grid'].format(year=year, date=date))

        print(f"\n\nProcessing {date}")
        start_time = time.time()

        # Ground / Plants extraction
        print("[INFO] Extracting ground cloud")
        ground_cloud = PointCloudGroundPlant.extract_ground_by_grid_min(cloud)

        print("[INFO] Extracting plant cloud")
        plant_cloud = PointCloudGroundPlant.subtract_clouds(cloud, ground_cloud, tol=1e-6)

        # Save clouds
        print("[INFO] Saving clouds")
        PointCloudGroundPlant.save_cloud(base_dir, date, year, suffix, plant_cloud, plant=True)
        PointCloudGroundPlant.save_cloud(base_dir, date, year, suffix, ground_cloud, plant=False)

        elapsed = time.time() - start_time
        print(f"[INFO] {date} processed in {elapsed:.2f}s ({elapsed/60:.2f} min)")


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, 'config.yaml')
    config = load_config(config_path)
    get_ground_and_plant_pointclouds(config, base_dir)


if __name__ == "__main__":
    main()
