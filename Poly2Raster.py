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
arcpy.env.workspace = os.getcwd()+"/InputData"

# geodatabases
# ------------------ Fields to rasterize -------------------------#
# NCC_BoPs_v1.1.gdb --> ["BType1","BType2","DepthCode"]
# SalTemp.gdb --> 	["spr.Sal","rng.Sal","spr.Temp","rng.Temp"]
# Currents.gdb     --> 	["spr.MnSp","rng.MnSp","spr.MaxSp","rng.MaxSp","spr.Stres","rng.Stress"]
# Fetch.gdb   --> 	["fetchNW","fetchSE","fetchMax","fetchMean","distLand"]

# ------------------------------------#
# Loop through environmental geodatabases
geo = ["SalTemp.gdb","Currents.gdb","NCC_BoPs_v1.1.gdb","Fetch.gdb"]
for g in geo:

	# Get layer basename
	desc = arcpy.Describe(g)
	evname = desc.baseName

	# Set fields and layer name
	if evname == "SalTemp":
		inLayer = evname+"_Interp"
		fields = ["spr_Sal","rng_Sal","spr_Temp","rng_Temp"]
	elif evname == "Fetch":
		inLayer = evname+"_Interp"
		fields = ["fetchNW","fetchSE","fetchMax","fetchMean","distLand"]
	elif evname == "Currents":
		inLayer = evname+"_Interp"
		fields = ["spr_MnSp","rng_MnSp","spr_MaxSp","rng_MaxSp","spr_Stress","rng_Stress"]
	elif evname == "NCC_BoPs_v1.1":
		inLayer = "BoP18_Merged"
		fields = ["BType1","BType2","DepthCode"]

	# set appropriate cell size to match lowest resolution of the native point data
	if evname == "SalTemp" or evname == "Currents":
		cellSize =  100.0
	elif evname == "Fetch":
		cellSize =  50.0
	elif evname == "NCC_BoPs_v1.1":
		cellSize =  20.0

	# Input feature
	inFeature = "Polygons/"+g+"/"+inLayer

	# loop through fields
	for f in fields:

		# output
		if evname == "SalTemp" or evname == "Currents" or evname == "Fetch":
			outRaster = "Rasters/Original/"+f+".tif"
		elif evname == "NCC_BoPs_v1.1":
			outRaster = "Rasters/BoP_Aligned/"+f+".tif"

		# Set variables
		assignmentType = "MAXIMUM_COMBINED_AREA"
		priorityField = ""

		# Execute PolygonToRaster
		arcpy.PolygonToRaster_conversion(inFeature, f, outRaster, assignmentType, priorityField, cellSize)
