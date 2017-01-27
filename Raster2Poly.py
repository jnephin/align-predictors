# Name: Raster2Poly.py
# Created on: 2016-12-20
# Edited on: 2017-01-25
# Author: Jessica Nephin

# Description: Converts raster layers to polygon features

# Import modules
import os
import arcpy

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# move up one directory
os.chdir('..')

# Set environment settings
arcpy.env.workspace = os.getcwd()+"/InputData"
gdbpath = os.getcwd()+"/InputData/Polygons"

# ------------------------------------#
# loop through geodatabase to create
gdb = ["Chla.gdb","Bathy.gdb"]
for g in gdb:

	# Create geodatabase
	arcpy.CreateFileGDB_management (gdbpath, g)

	# gdb layers
	if g == "Bathy.gdb":
		rasters = ["ArcRug","bathy","BBPI","MBPI","FBPI","Slope"]
	elif g == "Chla.gdb":
		rasters = ["Chla_mean","Bloom_Freq"]

	# ------------------------------------#
	# loop through raster
	for r in rasters:

		# Input
		name = "Rasters/Original/"+r+".tif"

		# Output
		out = "Polygons/"+g+"/"+r

		# Multiply raster
		tmpRas = arcpy.sa.Raster(name) * 100000

		# Convert to Integer
		intRas = arcpy.sa.Int(tmpRas)

		# Execute PolygonToRaster
		arcpy.RasterToPolygon_conversion (intRas, out, "NO_SIMPLIFY", "VALUE")

		# Add new attribute and divide value by 100000
		arcpy.AddField_management(out, r, "DOUBLE", 18, 11)
		arcpy.CalculateField_management (out, r, "!GRIDCODE! / 100000 ", "PYTHON_9.3")
