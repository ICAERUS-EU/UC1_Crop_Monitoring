import os
import sys
import time
import open3d as o3d
from tqdm import tqdm

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pointcloud.pointcloud_loader import PointCloudLoader
from extract_analysis.analysis import VolumeAnalysis
from grid.grid_operations import GridOperations
from utils.utils import load_json, load_config, save_json


def run_points_analysis(config, base_dir):
    io_cfg = config["io"]
    paths_cfg = config["paths"]
    years = config.get("years", ["2023", "2024"])
    dates = config.get("dates", [])
    down = config.get("downsample", True)
    skip_dates = config.get("skip_dates", [])

    suffix = "_down" if down else ""
    analysis_path = os.path.join(base_dir, f"data/analysis_data/points_analysis{suffix}.json")
    data = load_json(analysis_path)

    for date in tqdm(dates): 
        year = "20"+date[0:2]
        grid_base_dir = os.path.join(base_dir, f"data/grids/{year}")
        if not os.path.exists(grid_base_dir):
            print(f"[WARN] Grid directory not found: {grid_base_dir}")
            continue
        if date in data or date in skip_dates:
            continue

        # Paths
        if down:
            cloud_path = os.path.join(base_dir, io_cfg["downsample_dir"].format(suffix=suffix), f"{year}/vineyard_{date}{suffix}.txt")
        else:
            if date == '230518' or date=='240703':
                continue
            cloud_path = os.path.join(io_cfg["zenodo_base_dir"], year, date, "POINTCLOUDS", f"CROPPED_POINTCLOUD_{date}.txt")
        
        plant_path = f"{base_dir}/{io_cfg[f'plant_cloud_dir{suffix}']}/{year}/plant_cloud_{date}{suffix}.ply"
        if not os.path.exists(cloud_path) or not os.path.exists(plant_path):
            print(f"[SKIP] Missing cloud file for {date}")
            continue

        # Load cloud
        cloud = PointCloudLoader.load_cloud(cloud_path)
        plant_cloud = o3d.io.read_point_cloud(plant_path)

        # Load grid
        grid_path = os.path.join(base_dir, paths_cfg['grid'].format(year=year, date=date))
        line_sets = GridOperations.deserialize_line_sets(grid_path)

        print(f"\n\nProcessing {date}")
        start_time = time.time()

        # Total points analysis
        print("[INFO] Counting points in cloud")
        total_points_rows, points_per_parcel = VolumeAnalysis.get_total_points(cloud, line_sets)

        # Points in plant cloud
        print("[INFO] Counting points in plant cloud")
        total_points_plant_rows, points_per_parcel_plant = VolumeAnalysis.get_total_points(plant_cloud, line_sets)

        elapsed = time.time() - start_time
        print(f"[INFO] {date} processed in {elapsed:.2f}s ({elapsed/60:.2f} min)")

        # Store results
        data[date] = {
            "points_cloud": len(cloud.points),
            "points_rows": total_points_rows,
            "points_parcel": points_per_parcel,
            "points_cloud_plant": len(plant_cloud.points),
            "points_rows_plant": total_points_plant_rows,
            "points_parcel_plant": points_per_parcel_plant
        }

        # Save incremental results
        save_json(analysis_path, data)
        print(f"[INFO] {date} saved in {analysis_path}")


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, 'config.yaml')
    config = load_config(config_path)
    run_points_analysis(config, base_dir)


if __name__ == "__main__":
    main()
