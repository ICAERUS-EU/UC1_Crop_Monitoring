# 03 - PLANT LEAVES ANALYSIS

- **Description:** This code approaches some methods for performing analysis and detect early disease development in vineyard leaves.
- **Dataset:** [VINEYARD PLANT LEAVES IMAGES (SUMMER 2024)](https://zenodo.org/records/13944498)
- **Input:** Image size (120,160,3)
- **Output:** Cluster classification of leaves, VARI over time
- **Method:** Algorithmic approach
- **Type:** Clustering
- **Date:** 17/10/2024

This code showcases various approaches for analyzing vineyard leaves. It uses a dataset of 16 images, collected from the same locations over 8 different days during the summer of 2024. The leaves are labelled with a number, a letter and the concrete date when they were collected. 

The first approach focuses on detecting orange spots on the leaves, counting them, and calculating their total area. The image below shows an example of this classification. These characteristics help distribute the leaves as either healthy or unhealthy, depending on the number and area of these spots.

<p align="center"> <img src="https://github.com/user-attachments/assets/fe321b8e-1066-48ed-82a1-dca28293ffdd" width=700 height=396> </p>

Another important feature extracted is the VARI (Visible Atmospherically Resistant Index), which measures the greenness in RGB images—a key indicator of plant health. The VARI index ranges from -1 to 1, where values closer to 1 indicate higher green levels, typically associated with healthier plants. This graphs show the variation of VARI over time, leading to a decrease on this value in the end of the summer. 

<p align="center"> <img src="https://github.com/user-attachments/assets/6a8a2d4b-ea28-4ad2-ba22-4863f1438275" width=700 height=396> </p>

Finally, combining the number of orange spots, their area, and the VARI index, a KMeans clustering model is applied to group the leaves into three categories based on these values. Leaves with more orange spots, larger affected areas, and lower VARI index values are linked to unhealthy plants. The following image shows the expected outcome, with leaves at risk highlighted in yellow and those associated with poor health marked in red.

<p align="center"> <img src="https://github.com/user-attachments/assets/d6262d54-ac04-4789-adda-0272e755ae5a" width=700 height=396> </p>



## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)


## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
