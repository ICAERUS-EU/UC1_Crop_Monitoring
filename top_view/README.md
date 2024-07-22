# TOP-VIEW LEVEL CALCULATIONS 

The **top_view** approach contains the following calculations: 

## calculate_vegetation_indexes
Calculates different vegetation indexes for orthomosaic images of the vineyard area. For example, using the NIR orthomosaic image and the red spectral orthomosaic image, you can calculate the NDVI orthomosaic values: 
<p align="center">
  <img src="https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/assets/148956768/e7b47fef-4ab3-472c-ba5e-563a531c0135" style="width:75%; height:75%;">
</p>

## create_grid
It obtains a grid that divides the terrain between parcels as in the image: 
<p align="center">
  <img src="https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/assets/148956768/585db7b1-a607-4364-a087-3ceb79d38870" style="width:75%; height:75%;">
</p>


## NDVI_per_parcels
Using the NDVI image calculation and the grid information, you can divide the parcels depending on the NDVI levels. As the NDVI is greater, it is supposed to be more "greenery" in that part, so the plant should be healthier. Additionally, you can you any other vegetations index for this analysis.  

<p align="center">
  <img src="https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/assets/148956768/a27b4f2a-a02b-4c34-b739-972aba28ba5d" style="width:75%; height:75%;">
</p>
