import os
import sys
import time
import numpy as np
import open3d as o3d
from tqdm import tqdm

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extract_analysis.analysis import ColorAnalysis
from grid.grid_operations import GridOperations
from utils.utils import load_json, load_config, save_json


def run_ndvi_analysis(config, base_dir):
    io_cfg = config["io"]
    paths_cfg = config["paths"]
    years = config.get("years", ["2023", "2024"])
    dates = config.get("dates", [])
    skip_dates = config.get("skip_dates", [])

    suffix = '_down' if config.get("downsample", True) else ""
    analysis_path = os.path.join(base_dir, f"data/analysis_data/NDVI_analysis{suffix}.json")
    data = load_json(analysis_path)
    lut = ColorAnalysis.build_rainbow_lut()  # Build LUT once

    for date in tqdm(dates): 
        year = "20"+date[0:2]
        if date in data or date in skip_dates:
            continue

        plant_path = os.path.join(base_dir, io_cfg[f"plant_cloud_dir_NDVI{suffix}"], f"{year}/plant_cloud_{date}_NDVI{suffix}.ply")
        
        if not os.path.exists(plant_path):
            print(f"\n[SKIP] Missing NDVI plant cloud for {date}")
            continue

        plant_cloud = o3d.io.read_point_cloud(plant_path)
        grid_path = os.path.join(base_dir, paths_cfg['grid'].format(year=year, date=date))
        line_sets = GridOperations.deserialize_line_sets(grid_path)

        print(f"\n\nProcessing {date}")
        start_time = time.time()

        ndvi_parcels, mean_ndvi = ColorAnalysis.mean_ndvi_per_parcel(plant_cloud, line_sets, lut)

        elapsed = time.time() - start_time
        print(f"[INFO] {date} processed in {elapsed:.2f}s ({elapsed/60:.2f} min)")

        data[date] = {
            "color_plant": mean_ndvi,
            "color_parcel_plant": ndvi_parcels
        }

        save_json(analysis_path, data)
        print(f"[INFO] {date} saved in {analysis_path}")


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, 'config.yaml')
    config = load_config(config_path)
    run_ndvi_analysis(config, base_dir)


if __name__ == "__main__":
    main()
