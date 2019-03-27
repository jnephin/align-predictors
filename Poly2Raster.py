# Name: Poly2Raster.py
# Created on: 2016-12-16
# Edited on: 2017-01-26
# Author: Jessica Nephin

# Description: Converts polygon features to a raster dataset.

# Import modules
import arcpy
import os

# move up one directory
os.chdir('..')

# allow overwriting
arcpy.env.overwriteOutput = True

# Set environment settings
arcpy.env.workspace = os.getcwd()


# ------------------------------------#
# Loop through environmental geodatabases
geo = ["Fetch_NCC_bop.gdb",] #"NCC_BoPs_v1.1.gdb","Fetch.gdb","SalTemp.gdb","Currents.gdb"]
for g in geo:

	# Get layer basename
	desc = arcpy.Describe("Data/NCC_nearshore/InputData/Polygon/"+g)
	evname = desc.baseName

	# Set fields and layer name
	if evname == "SalTemp":
		inLayer = evname+"_Interp"
		fields = ["spr_Sal","rng_Sal","spr_Temp","rng_Temp"]
	elif evname == "Fetch_NCC_bop":
		inLayer = evname+"_Interp"
		fields = ["distLand", "fetchSum" ] # fetchNW","fetchSE","fetchMax","fetchMean"]
	elif evname == "Currents":
		inLayer = evname+"_Interp"
		fields = ["spr_MnSp","rng_MnSp","spr_MaxSp","rng_MaxSp","spr_Stres","rng_Stress"]
	elif evname == "NCC_BoPs_v1.1":
		inLayer = "BoP"
		fields = ["BType","DepthBin"]

	# set appropriate cell size to match lowest resolution of the native point data
	if evname == "SalTemp" or evname == "Currents":
		cellSize =  100.0
	elif evname == "Fetch_NCC_bop":
		cellSize =  20.0
	elif evname == "NCC_BoPs_v1.1":
		cellSize =  20.0

	# Input feature
	inFeature = "Data/NCC_nearshore/InputData/Polygon/"+g+"/"+inLayer

	# loop through fields
	for f in fields:

		# output
		if evname == "SalTemp" or evname == "Currents" or evname == "Fetch_NCC_bop":
			outRaster = "Data/NCC_nearshore/InputData/Raster/Original/"+f+".tif"
		elif evname == "NCC_BoPs_v1.1":
			outRaster = "AlignedData/Rasters/"+f+".tif"

		# Set variables
		assignmentType = "MAXIMUM_COMBINED_AREA"
		priorityField = ""

		# Execute PolygonToRaster
		arcpy.PolygonToRaster_conversion(inFeature, f, outRaster, assignmentType, priorityField, cellSize)
