import os
import sys
import time
import numpy as np
import open3d as o3d
from tqdm import tqdm

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pointcloud.pointcloud_loader import PointCloudLoader
from extract_analysis.analysis import HeightAnalysis
from grid.grid_operations import GridOperations
from utils.utils import load_json, load_config, save_json


def run_height_analysis(config, base_dir):
    io_cfg = config["io"]
    paths_cfg = config["paths"]
    down = config.get("downsample", True)
    dates = config.get("dates", [])
    skip_dates = config.get("skip_dates", [])

    # Sufixes
    suffix = '_down' if down else ""
    analysis_path = os.path.join(base_dir, f"data/analysis_data/height_analysis{suffix}.json")
    data = load_json(analysis_path)
    
    for date in tqdm(dates): 
        year = "20"+date[0:2]
        if date in data or date in skip_dates:
            continue

        # Paths
        if down:
            cloud_path = os.path.join(base_dir, io_cfg["downsample_dir"].format(suffix=suffix), f"{year}/vineyard_{date}{suffix}.txt")
        else:
            cloud_path = paths_cfg["pointcloud"].format(zenodo_base=io_cfg["zenodo_base_dir"], year=year, date=date, suffix=suffix)
        plant_path = f"{base_dir}/{io_cfg[f'plant_cloud_dir{suffix}']}/{year}/plant_cloud_{date}{suffix}.ply"
        if not os.path.exists(cloud_path) or not os.path.exists(plant_path):
            print(f"[SKIP] Missing files for {date}")
            continue
        
        # Load clouds
        cloud = PointCloudLoader.load_cloud(cloud_path)
        plant_cloud = o3d.io.read_point_cloud(plant_path)

        # Load grid
        grid_path = f"{base_dir}/{paths_cfg['grid'].format(year=year, date=date)}"
        line_sets = GridOperations.deserialize_line_sets(grid_path)

        print(f"\n\nProcessing {date}")
        start_time = time.time()

        # Height analysis
        height_cloud = HeightAnalysis.calculate_height(np.asarray(cloud.points))
        height_plant_cloud = HeightAnalysis.calculate_height(np.asarray(plant_cloud.points))
        height_rows, height_parcels = HeightAnalysis.get_height_points(cloud, line_sets)
        height_plant_rows, height_plant_parcels = HeightAnalysis.get_height_points(plant_cloud, line_sets)

        # Store results
        data[date] = {
            "height_cloud": height_cloud,
            "height_rows": height_rows,
            "height_parcel": height_parcels,
            "height_cloud_plant": height_plant_cloud,
            "height_rows_plant": height_plant_rows,
            "height_parcel_plant": height_plant_parcels,
        }

        save_json(analysis_path, data)
        elapsed = time.time() - start_time
        print(f"[INFO] {date} processed in {elapsed:.2f}s ({elapsed/60:.2f} min)")
        print(f"[INFO] {date} saved in {analysis_path}") 


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, 'config.yaml')
    config = load_config(config_path)
    run_height_analysis(config, base_dir)


if __name__ == "__main__":
    main()
