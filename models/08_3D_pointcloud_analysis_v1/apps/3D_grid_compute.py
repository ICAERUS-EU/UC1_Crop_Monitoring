"""
Main application for 3D grid computation and alignment from point clouds and orthomosaics
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grid.grid_processor import GridProcessor
from utils.utils import load_config


def main():
    
    # Load configuration from YAML
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(base_dir, 'config.yaml')
    config = load_config(config_path)
    
    # Create and run processor
    processor = GridProcessor(config, base_dir)
    processor.compute_grid()


if __name__ == "__main__":
    main()