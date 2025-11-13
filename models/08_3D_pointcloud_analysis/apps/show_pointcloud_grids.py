"""
Main application for 3D grid computation and visualization from point clouds and orthomosaics.
"""
import os
import sys
import open3d as o3d

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grid.grid_operations import GridOperations
from pointcloud.pointcloud_loader import PointCloudLoader
from utils.utils import load_config


# ============================================================
# VISUALIZATION FUNCTION
# ============================================================
def visualize_original_pointclouds(config, base_dir):
    """
    Visualiza nubes de puntos desde datasets almacenados en ZENODO.
    Usa rutas y sufijos definidos en el archivo YAML.
    """
    io_cfg = config["io"]
    paths_cfg = config["paths"]
    dates = config.get("dates", [])
    skip_dates = config.get("skip_dates", [])
    down = config.get("downsample", True)
    ndvi = config.get("ndvi", False)
    suffix_grid = '_NDVI' if ndvi else ""
    suffix = ""
    if down and ndvi: 
        suffix = '_NDVI_down'
    elif down:
        suffix = '_down'

    if not down and ndvi:
        print("[WARNING] NDVI visualization only available for downsampled files. Switching to downsampled mode.")
        suffix = '_NDVI_down'
        down = True
    
    for date in dates: 
        if date in skip_dates: 
            continue
        year = "20"+date[0:2]
        print(f"\n\Loading {date} from year {year}")

        # Construct paths
        if down:
            cloud_path = f"{base_dir}/data/vineyards{suffix}/{year}/vineyard_{date}{suffix}.txt"
        else: 
            cloud_path = paths_cfg["pointcloud"].format(
                zenodo_base=io_cfg["zenodo_base_dir"], year=year, date=date)            
        grid_path = f"{base_dir}/data/grids{suffix_grid}/{year}/grid_{date}{suffix_grid}.npz"

        if not os.path.exists(cloud_path) or not os.path.exists(grid_path):
            print(f"[SKIP] Missing files for {date}")
            continue

        # Load data
        cloud = PointCloudLoader.load_cloud(cloud_path)
        line_sets = GridOperations.deserialize_line_sets(grid_path)

        # Visualize
        print(f"[INFO] Showing date {date}")
        o3d.visualization.draw_geometries([cloud] + line_sets)


# =================================================
# MAIN ENTRY POINT
# ============================================================
def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(base_dir, 'config.yaml')
    config = load_config(config_path)

    visualize_original_pointclouds(config, base_dir)


if __name__ == "__main__":
    main()
