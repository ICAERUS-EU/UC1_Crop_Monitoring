"""
Main application for downsampling vineyard point clouds.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pointcloud.pointcloud_downsampler import PointCloudDownsampler
from utils.utils import load_config


def main():

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(base_dir, 'config.yaml')
    config = load_config(config_path)

    cloud_downsample = PointCloudDownsampler(config, base_dir)
    cloud_downsample.process_downsample()


if __name__ == "__main__":
    main()
