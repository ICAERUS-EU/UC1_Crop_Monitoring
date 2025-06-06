# 03 - PLANT LEAVES ANALYSIS

- **Description:** This code approaches some methods for performing analysis and detect early disease development in vineyard leaves using color detection, VARI index and clustering algorithms.
- **Dataset:** [VINEYARD PLANT LEAVES IMAGES (SUMMER 2024)](https://zenodo.org/records/13944498)
- **Input:** Image size (120,160,3)
- **Output:** Cluster classification of leaves, VARI over time
- **Method:** Algorithmic approach
- **Type:** Clustering
- **Date:** 17/10/2024

This code showcases various approaches for analyzing vineyard leaves. It uses a dataset of 16 images, collected from the same locations over 8 different days during the summer of 2024. The leaves are labelled with a number, a letter and the concrete date when they were collected. 

The first approach focuses on detecting orange spots on the leaves, counting them, and calculating their total area. The image below shows an example of this classification. These characteristics help distribute the leaves as either healthy or unhealthy, depending on the number and area of these spots.

<p align="center"> <img src="https://github.com/user-attachments/assets/34685e3d-be21-420c-aaf7-cc2988b2d3dd" </p>

Another important feature extracted is the VARI (Visible Atmospherically Resistant Index), which measures the greenness in RGB images—a key indicator of plant health. The VARI index ranges from -1 to 1, where values closer to 1 indicate higher green levels, typically associated with healthier plants. This graphs show the variation of VARI over time, leading to a decrease on this value in the end of the summer. 

<p align="center"> <img src="https://github.com/user-attachments/assets/739a591d-0667-4bb9-9b39-fe31f5efdb52" </p>

Finally, combining the number of orange spots, their area, and the VARI index, a KMeans clustering model is applied to group the leaves into three categories based on these values. Leaves with more orange spots, larger affected areas, and lower VARI index values are linked to unhealthy plants. The following image shows the expected outcome, with leaves at risk highlighted in yellow and those associated with poor health marked in red.

<p align="center"> <img src="https://github.com/user-attachments/assets/5d1198bd-26ca-4209-94f6-c400a1e13786"</p> 



## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)


## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
