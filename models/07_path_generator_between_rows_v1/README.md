# 07 - PATH GENERATOR BETWEEN ROWS

## 🌿 Overview

This repository contains code for generating a GPS-based path between vineyard rows. The generated path is saved as a list of GPS coordinates that 
recreate the desired flight path for a drone. These coordinates can be used to fly the drone at low altitude to capture images of the plants.

The output file, **drone_path_gps.json**, should be converted to the required YAML format (*conversion code to be uploaded*). Once converted, it can be used directly for simulating a drone flight adjusting the initial coordinates according to the simulation environment.

 ## 🗂️ Structure

- **src:** 
  - **OrthomosaicProcessor.py**: class for loading, resizing, and processing orthomosaic images and masks.
  - **PathGenerator.py**: class to compute and visualize optimal drone paths across row segments, with support for image overlay and GPS conversion.
  - **utils.py**: it contains helper functions for reading and saving JSON files. 
  - **VineyardRowDetector.py**: class for detecting vineyard rows from an orthomosaic image. 
- **README.md**: explanation of the repository and usage. 
- **generate_drone_path_between_rows.py**: main code to execute. It detects the rows and generate the gps path between them.  
- **requirements.txt**: file to easily install the libraries. 


## 📄 Dataset 

The data needed for this code is included in the [UC1 DATA FOLDER GITHUB](https://zenodo.org/records/11195994) and should be saved into the data folder of this repository. This data includes already the drone gps path saved. 


## 💻 Requirements

- **Environment configuration**: please install the *requirements.txt* file into a conda environment to have the necessary libraries to execute the code.
- **Data**: download the [UC1 DATA FOLDER GITHUB](https://zenodo.org/records/11195994) to have the orthomosaic image used for detecting the rows and generating the drone path. 

## ⚙️ Parameters

The parameters are defined directly in the code. 

- **Data paths**: define the data path to read the orthomosaic image and where to save the coordinates defining the row lines, row contours and drone gps path. 
- **Variables**: variables are defined inside the code and are adjusted for this purpose. 


## 🚀 Usage
For generating the drone path between rows, just type the following command in the _07_path_generator_between_rows_v1_ directory with the environment active: 

```
python generate_dron_path_between_rows.py
```

First of all, the orthomosaic image and its mask are read. Then it uses the class VineyardRowDetector to detect the rows of the vineyards in the orthomosaic image. This is done in the following manner: 

- There is already a row definition with its coordinates (2250, 3453) and (4876, 2855). This coordinates were obtained setting the *select_points* variable to *True* and manually selecting the first row. The points are scalated automatically in the mouse callback.
- Then, from this row, the rest of the rows are generating by knowing the distance between rows and with an arbitrary wide and length (*get_parallel_rows*).
- When all the rows are drawn we filter them using the orthomosaic mask to adjust them to the image (*filter_rows*).


<!-- <p align="center"> <img src="https://github.com/user-attachments/assets/8e5708b6-ee3b-4aff-a0b0-a78a25ccc337" alt="Row Image Example" width="45%"> <img src="https://github.com/user-attachments/assets/9792253b-f08f-40bb-99c9-055095e4af18" alt="Orthomosaic Image Example" width="45%"> </p> -->


- We detect the rows coordinates using contour detection and save also the lower line of this contour (*get_rows_coordinates*).

Now that we have the lines (saved in *rows* variable) that define each vineyard row, we can generate the path. The path will happen a little bit lower in the image, between each row and an optimized path should be generated. 

- The code uses the class PathGenerator, with *generate_path* function, that will build the path between rows in zigzag as the drone movement will be. Starting from the *current_line* it finds the closest row and moves in that direction taking into account the start and ending of each row. 


Once we have the path in pixel coordinates, it is changed to GPS coordinates using the transform matrix saved in the orthomosaic image. With the GPS coordinates, we transform them to the drone simulation format in YAML using **INCOMPLETE**, that includes the height and the type of movement and this can be used for moving the anafi drone in simulation or real life directly using the [04_drone_simulation_v1](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/models/04_drone_simulation_v1) code. 

- 



## 📊 Results
As a final result, we get the path generated in pixel coordinates and GPS coordinates and ready for flying the drone. 

Before, we have compute the rectangle contours that define each vineyard row in the image, which is saved in rows_contour_coordinates.json and the lower line of each row in rows_coordinates.json. 

The final path is shown in the following matplotlib image 


If we draw it over the orthomosaic image we can see how the drone will move between the vineyard rows: 

The drone_path_pixel.json is saved too. The final *drone_path_gps.json* is saved in the format shown in the image. The movement between points would be linear. 


> [!TIP]
> The **DETECT VINEYARD ROWS** section of the code can be comented as the *rows_coordinates.json* is already generated and can be just read and avoid executing the row detection functions.  


## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
