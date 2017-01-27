# GDB_RasterExport.py
# Created on:  2017-01-26
# Edited on: 2017-01-26
# Author: Jessica Nephin

# Export rasters from derived bathymetry geodatabase

# Import modules
import arcpy
import os
import re

# move up one directory
os.chdir('..')

# allow overwriting
arcpy.env.overwriteOutput = True

# Set environment settings
arcpy.env.workspace = os.getcwd()+"/InputData/Rasters/Original"

# geodatabase
gdb = "NCC_Bathy_Derived_Layers.gdb"


#--------------------------------------------------------------------------------#
# loop through raster layers
rasters = ["NCC_ArcRug","ncc_bathy","NCC_BBPI","NCC_MBPI","NCC_FBPI","NCC_Slope"]

for r in rasters:

# variables
	inRaster = gdb+"/"+r
	name = re.sub('NCC_|ncc_', '', r)
	outRaster = name+".tif"
	pt="32_BIT_FLOAT"
	f="TIFF"
	na=-3.4e+38

	# export rasters
	arcpy.CopyRaster_management(inRaster,outRaster, background_value=na, nodata_value=na, pixel_type=pt)
