import os
import sys
import open3d as o3d
import numpy as np 

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from visualizer.visualizer_color import VisualizerColor
from visualizer.visualizer_height import VisualizerHeight
from visualizer.visualizer_volume import VisualizerVolume
from visualizer.visualizer_points import VisualizerPoints
from visualizer.visualizer_pointcloud import VisualizerPointCloud

from pointcloud.pointcloud_loader import PointCloudLoader
from utils.utils import load_config, load_json


# ===========================================================
# COLOR VISUALIZATION
# ===========================================================
def run_color_visualization(config, base_dir, color_type, parcel_idx):
    """
    Load color analysis results and visualize color evolution 
    and parcel comparisons in 3D.
    """
    down = config.get("downsample", True)
    suffix = '_down' if down else ""
    analysis_path = os.path.join(base_dir, f"data/analysis_data/{color_type}_analysis{suffix}.json")
    print(f"[INFO] Reading color analysis data from {analysis_path}")

    # Load data
    raw_data = load_json(analysis_path)
    print("[INFO] Data successfully loaded")

    # Initialize visualizer
    vis = VisualizerColor(color_type, raw_data)

    # Show total and parcel-level color evolution
    print("[INFO] Displaying total and parcel color evolution")
    vis.show_total_color()
    vis.show_parcel_color(parcel_idx)

    print("[INFO] Starting 3D parcel visualization")



# ===========================================================
# HEIGHT VISUALIZATION
# ===========================================================
def run_height_visualization(config, base_dir, parcel_idx):
    down = config.get("downsample", True)
    suffix = "_down" if down else ""
    analysis_path = os.path.join(base_dir, f"data/analysis_data/height_analysis{suffix}.json")
    
    print(f"[INFO] Reading height analysis data from {analysis_path}")
    raw_data = load_json(analysis_path)

    print("[INFO] Data successfully loaded")
    vis = VisualizerHeight(raw_data)
    vis.show_total_height()
    vis.show_parcel_height(parcel_idx)

    print("[INFO] Height visualization complete.")



# ===========================================================
# VOLUME & DENSITY VISUALIZATION
# ===========================================================
def run_volume_visualization(config, base_dir, parcel_idx):
    """
    Load volume and density analysis results and visualize 
    total and parcel-level metrics.
    """
    down = config.get("downsample", True)
    suffix = "_down" if down else ""
    analysis_path = os.path.join(
        base_dir, f"data/analysis_data/volume_density_analysis{suffix}.json"
    )

    print(f"[INFO] Reading volume/density data from {analysis_path}")
    raw_data = load_json(analysis_path)
    print("[INFO] Data successfully loaded")

    vis = VisualizerVolume(raw_data)
    print("[INFO] Displaying total and parcel-level volume/density plots")

    vis.show_total_volume()
    vis.show_parcel_volume(parcel_idx)
    vis.show_total_density()
    vis.show_parcel_density(parcel_idx)

    print("[INFO] Volume & density visualization complete.")


# ===========================================================
# POINTS ANALYSIS VISUALIZATION
# ===========================================================
def run_points_visualization(config, base_dir, parcel_idx):
    """
    Load point count analysis results and visualize total,
    row-level, and parcel-level distributions in 3D.
    """
    down = config.get("downsample", True)

    suffix = "_down" if down else ""
    analysis_path = os.path.join(
        base_dir, f"data/analysis_data/points_analysis{suffix}.json"
    )

    print(f"[INFO] Reading points analysis data from {analysis_path}")
    raw_data = load_json(analysis_path)
    print("[INFO] Data successfully loaded")

    vis = VisualizerPoints(raw_data)
    vis.show_total_points()
    vis.show_rows_points()
    vis.show_parcel_points(parcel_idx)

    print("[INFO] Points visualization complete.")


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, 'config.yaml')
    config = load_config(config_path)
    parcel_idx = config.get("parcel_idx", 0)
    color_type = config.get("color_type", "VARI")
    vis3D = VisualizerPointCloud(config, base_dir)

    # Select data to visualize
    mode = config.get("mode", "points")  
    if mode in ("color", "all"):
        print("\n[MODE] COLOR VISUALIZATION")
        run_color_visualization(config, base_dir, color_type, parcel_idx)

    if mode in ("height", "all"):
        print("\n[MODE] HEIGHT VISUALIZATION")
        run_height_visualization(config, base_dir, parcel_idx)

    if mode in ("volume", "all"):
        print("\n[MODE] VOLUME/DENSITY VISUALIZATION")
        run_volume_visualization(config, base_dir, parcel_idx)

    if mode in ("points", "all"):
        print("\n[MODE] POINTS COUNTING VISUALIZATION")
        run_points_visualization(config, base_dir, parcel_idx)

    # Show 3d parcels and pointclouds
    vis3D.show_3d_parcels()

if __name__ == "__main__":
    main()
