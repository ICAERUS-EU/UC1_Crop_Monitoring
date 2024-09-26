# TOP-VIEW LEVEL CALCULATIONS 

The **top_view** approach contains the following calculations: 

## create_grid
It obtains a grid that divides the terrain between parcels as in the images: 
<p align="center">
  <img src="https://github.com/user-attachments/assets/804df86c-ed36-4e7a-b8da-de72477af1e5" style="width:75%; height:75%;display:inline-block; margin:0;">
  <img src="https://github.com/user-attachments/assets/cc053c9a-c05e-4daa-9c10-f4fec797c747" style="width:75%; height:75%;display:inline-block; margin:0;">
</p>

## create_grid_aligned
It obtains a grid that divides the terrain between parcels in an aligned orthomosaic vineyard as in the images:
<p align="center">
  <img src="https://github.com/user-attachments/assets/b00022ac-f330-4762-bd6e-74b137f1a1b5" style="width:75%; height:75%;display:inline-block; margin:0;">
  <img src="https://github.com/user-attachments/assets/2f12a972-b1cf-4218-8b00-3437f01a2aa7" style="width:75%; height:75%;display:inline-block; margin:0;">
</p>

## calculate_vegetation_indexes
Calculates different vegetation indexes for orthomosaic images of the vineyard area. For example, using the NIR orthomosaic image and the red spectral orthomosaic image, you can calculate the NDVI orthomosaic values: 
<p align="center">
  <img src="https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/assets/148956768/e7b47fef-4ab3-472c-ba5e-563a531c0135" style="width:75%; height:75%;">
</p>

## NDVI_per_parcels
Using the NDVI image calculation and the grid information, you can divide the parcels depending on the NDVI levels. As the NDVI is greater, it is supposed to be more "greenery" in that part, so the plant should be healthier. Additionally, you can you any other vegetations index for this analysis.  

<p align="center">
  <img src="https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/assets/148956768/a27b4f2a-a02b-4c34-b739-972aba28ba5d" style="width:75%; height:75%;">
</p>
