# TOP-VIEW LEVEL CALCULATIONS 

The **top_view** approach contains the following calculations: 

## create_grid
It obtains a grid that divides the terrain between parcels as in the images: 
<p align="center">
  <img src="https://github.com/user-attachments/assets/f8def1d6-c706-4435-85b8-517dafbf31d2" style="width:75%; height:75%;display:inline-block; margin:0;">
  <img src="https://github.com/user-attachments/assets/3f59b07d-cdc5-4c24-aa3c-e1abda4814a9" style="width:75%; height:75%;display:inline-block; margin:0;">
</p>

## create_grid_aligned
It obtains a grid that divides the terrain between parcels in an aligned orthomosaic vineyard as in the images:
<p align="center">
  <img src="https://github.com/user-attachments/assets/e05b5671-3e85-49e5-b94f-ec62ed9cfa8f" style="width:75%; height:75%;display:inline-block; margin:0;">
  <img src="https://github.com/user-attachments/assets/20386eba-575d-4da3-b558-cbc3a3d16d9c" style="width:75%; height:75%;display:inline-block; margin:0;">
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
