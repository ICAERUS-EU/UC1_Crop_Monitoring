# 08 - 3D POINTCLOUD ANALYSIS

## 🌿 Overview

This repository contains a collection of models designed to analyze pointclouds using information such as volume, height, VARI, NDVI, and point density. These models generate a 3D grid that matches the 2D orthomosaic grid and produce graph visualizations to assess differences in the 3D reconstruction of vineyards over time.


 ## 🗂️ Structure

- **apps/** contains all the models that can be run. 
  - `3D_grid_computer.py`: main code to generate the 3D grid aligned with the pointcloud for analysing 3D parcels. 
  - `3D_pointcloud_downsample.py`: main code to remove outliers, downsample and standardized the pointclouds .
  - `extract_height_data.py`: extracts height data from a pointcloud for later analysis (`visualize_data.py`). 
  - `extract_NDVI_data.py`: extracts NDVI data from a pointcloud for later analysis (`visualize_data.py`).
  - `extract_points_data.py`: extracts points counting data from a pointcloud for later analysis (`visualize_data.py`).
  - `extract_VARI_data.py`: extracts VARI data from a pointcloud for later analysis (`visualize_data.py`).
  - `extract_volume_data.py`: extracts volume and density data from a pointcloud for later analysis (`visualize_data.py`).
  - `get_ground_and_plant_pointclouds.py`: main code to separate plants from ground and saved these pointclouds. Useful for pointclouds alignment and plant analysis.  
  - `show_pointcloud_grids.py`: shows the 3D grids generated in the pointlcouds. 
  - `visualize_data.py`: generates 2D analysis graphs over time of the extracted data. 
- **data/**: data folder that contains downsampled pointclouds, NDVI downsampled pointclouds, grids definitions, plants pointclouds, ground pointclouds, analysis data, etc.   
- **extract_analysis/**:
  - `analysis.py`: it contains the auxiliar classes to extract the pointcloud data. 
- **grid/**: codes to compute the 3D grid using the 2D grid as reference. 
  - `grid_alignment.py`
  - `grid_operations.py`
  - `grid_processor.py`
- **orthomosaic/**: loads the orthomosaic to align with the pointcloud and the 2D grid to generate the 3D grid. 
  - `orthomosaic_loader.py`: 
- **pointcloud/**: .
  - `pointcloud_downsampler.py`: code for performing the outlier removal and downsample of the point clouds. 
  - `pointcloud_ground_plants.py`: code to extract the ground pointclouds and plant point clouds. 
  - `pointcloud_loader.py`: to load and orient pointclouds. 
- **utils/**:  
  - `utils.py`: some utils functions to load files and tranform vectors. 
- **visualizer/**: code with clases to generate graphs and 3D visualization for the analysis data. 
  - `visualizer_color.py`
  - `visualizer_height.py`
  - `visualizer_pointcloud.py` 
  - `visualizer_points.py` 
  - `visualizer_volume.py` 
- `config.yaml`: paths and variables to run the models. 
- `README.md`: explanation of the repository and usage. 
- `requirements.txt`: file to easily install the libraries. 


## 📄 Dataset 

The data required for this code is included in the [UC1 DATA FOLDER - 3D POINTCLOUD ANALYSIS]().With this dataset, you can directly visualize the grids using `show_pointcloud_grids.py` and explore the analysis results with `visualize_data.py` without running the data extraction scripts. Alternatively, you can run the main `extract` scripts from the **apps/** folder in `down` mode if you want to generate the extracted data yourself. This data folder should be located at the same level as **apps/**, **extract_analysis/**, etc.

If you want to work with the original pointclouds to perform downsampling or extract 3D grids, you should download the vineyard datasets for each date you wish and you will have access to the CROPPED_POINTCLOUDS, CROPPED_NDVI and CROPPED_ORTHOMOSAICS. 

## 💻 Requirements

- **Environment configuration**: please install the *requirements.txt* file into a conda environment to have the necessary libraries to execute the code.
- **Data**: download the [UC1 DATA FOLDER - 3D POINTCLOUD ANALYSIS]() and Vineyards data for a specific date. if you would like to use the CROPPED_POINTCLOUDS or CROPPED_ORTHOMOSAICS and CROPPED_NDVI.

## ⚙️ Parameters

The parameters are defined in the `config.yaml`. 

- **Data paths**: specify the relative paths for the UC1 data folder or template paths. You should also set the Zenodo base directory, which is where the original cropped pointclouds, orthomosaics, and related data are stored on your computer.
- **Variables**: Control which data to process and how. Parameters include:
   - `years`: specific years to process (list of years). - _Not used._
   - `dates`: specific dates to process (list of dates.
   - `skip_dates`: dates or items to skip (list of dates).   
   - `showcase_dates`: select which data to visualize in 3D (list of dates).
   - `parcel_idx`: select which parcel to process (0-max parcels number).
   - `downsample`: whether to use downsampled data (true, false).
   - `ndvi`: use NDVI data or RGB data (true, false).
   - `mode`: select which data to visualize ('all', 'color', 'height', 'volume', 'points').
   - `color_type`: choose the type of color analysis to perform ('VARI' or 'NDVI').


## 🚀 Usage

Before executing any code, make sure to specify in `config.yaml` the type of data you would like to process (downsample, ndvi, etc). Make sure that the dataset is saved at the same level as the **apps/** folder with the name **data**. Modify any path necessary to refer to your data. This will be necessary for the original pointcloud zenodo data for downsampling datasets (`zenodo_base_dir` in `config.yaml`). Then, just type the python command in the `08_3D_pointcloud_analysis` with the environment active. For example, to visualize the 3D graphs data run: 

```
python visualize_data.py
```

You can execute any code inside the apps folder. 



## 📊 Results
As a final result, this is what we get from each one of the main codes:

  - `3D_grid_computer.py`  
A grid computation is saved in **data/grids/** or **data/grids_NDVI/**, depending on whether NDVI is active, along with a visualization of the generated 3D grid.

    
  - `3D_pointcloud_downsample.py`  
   A downsampled, aligned version of a pointcloud, with a outlier removal process. They are is saved in the folders with a suffix `down` in the name. 
  

  - `extract_height_data.py`, `extract_NDVI_data.py`, `extract_points_data.py`, `extract_VARI_data.py`, `extract_volume_data.py`   
   A JSON file with the data saved saved in /data/analysis_data/**.

Example for `height_data_down.json`:   
```json
{
    "230421": {
        "height_cloud": 7.554000000000002,
        "height_rows": 1.0698495800000005,
        "height_parcel": [
            0.8220000000000027,
            0.7536964700000096
        ],
        "height_cloud_plant": 7.7745591735839845,
        "height_rows_plant": 0.7582083984375003,
        "height_parcel_plant": [
            0.5721351623535157,
            0.48289794921875007
        ]
    }
}
```
  
  - `get_ground_and_plant_pointclouds.py`  
Two new point clouds were created: one contains the ground part of the vineyard, and the other contains the plant part. They are used for grid alignment and computing 3D analysis data.

   
  
  - `show_pointcloud_grids.py`  
A visualization of the 3D grids with the point clouds, as shown in the image:

  
  
  - `visualize_data.py`  
Generates 2D graphs showing how the point cloud analysis data changes over time. It also displays a comparison of the selected `parcel_idx over` time alongside the 3D model of these parcels and point clouds (`showcase_dates`).





<p align="center"> <img src="https://github.com/user-attachments/assets/1a0d1eec-85a0-48a9-a6af-69d46f94b503" alt="Row Image Example" width="60%"></p>







> **📝 NOTE:** Points analysis is conditions by resolution in Agisoft processing. It is always better to use the downsampled pointclouds for the graphs analysis as the data is more normalized. NDVI data is available for a limited number of dates. 


## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
