 Author:       Jessica Nephin  
 Affiliation:  IOS, Fisheries and Oceans Canada (DFO)  
 Group:        Marine Spatial Ecology & Analysis, Ecosystems Science Division  
 Address:      9860 West Saanich Road, Sidney, British Columbia, V8L 4B2, Canada  
 Contact:      e-mail: jessica.nephin@dfo-mpo.gc.ca | tel: 250.363.6564  


Combining environmental data layers
===========================

1) Copy polygon environmental geodatabases (e.g. SalTemp.gdb and NCC_BoPs_v1.1.gdb)
    from their home directories into 'InputData/Polygons'

2) Copy raster environmental layers (e.g. Chla_mean and NCC_Bathy_Derived_Layers.gdb)
    from their home directories into 'InputData/Rasters'

3) Clip BoP to NCC_Nearshore_Area_BoP and convert factors with BoPclip.py


Polygons
--------

1) Export layers from NCC_Bathy_Derived_Layers.gdb as GeoTiffs with 'GDB_RasterExport.py'

2) Convert raster layers into polygons with 'Raster2poly.py'

3) Perform overlay of environmental data onto BoPs with 'Env2Bop.py'. Final BoP layer
    including all environmental data is located in 'AlignedData/Polygons'.


Rasters
-------

1) Convert polygons to rasters as GeoTiffs with 'Poly2Raster.py'

2) Resample all rasters that didn't originate from BoP polygons to the resolution of BoPs.
    Align rasters to the spatial extent of BoP rasters while preforming the resample
    with 'ResampleGdal.sh'

3) Mask all rasters using a BoP raster layer that is clipped with a coastline polygon to limit
    the data to the nearshore BoP area. Export rasters as GeoTiffs to 'AlignedData/Rasters
    with 'MaskConvert.R' or 'Mask.py' (faster).

4) Calculate stats and build pyramids with 'Pyramids.sh'
