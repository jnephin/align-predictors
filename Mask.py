
# Import system modules
import os
import arcpy
from arcpy.sa import *

# set workspace
#os.chdir("D:/Projects/Combine_EnvData")

# region
region = "NCC_nearshore"

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# overwriteOutput
arcpy.env.overwriteOutput = True

# Set raster to mask that will be used as mask for all others
#ras = os.getcwd()+"/Data/"+region+"/InputData/Raster/Resampled/substrate.tif"
rasterMask = os.getcwd()+"/Data/"+region+"/AlignedData/Raster/substrate.tif"

# mask
#inMask =  os.getcwd()+"/Data/"+region+"/Boundary/SDM_offshore_model_domain.shp"
inMask = os.getcwd()+"/Data/"+region+"/Boundary/NCC_Nearshore_Area_BoP_buffer20m.shp"

# Set raster extent
boundary = arcpy.Describe(inMask)
ext = boundary.extent
arcpy.env.extent = ext
#
# # Clip with polygon
# rasterMask = ExtractByMask(ras, inMask)
# # output name
# outfilename = os.getcwd()+"/Data/"+region+"/AlignedData/Raster/tmp/substrate.tif"
# # Save the output
# rasterMask.save(outfilename)

# List rasters
arcpy.env.workspace = os.getcwd()+"/Data/"+region+"/InputData/Raster/Resampled"
rasters = arcpy.ListRasters("*", "TIF")

#------------------------------------------------------------------#
# Mask each raster in resampled directory
for r in rasters:

    # Clip with polygon
    outExtractByMask = ExtractByMask(r, rasterMask)
    # output name
    outfilename = os.getcwd()+"/Data/"+region+"/AlignedData/Raster/"+r
    # Save the output
    outExtractByMask.save(outfilename)
