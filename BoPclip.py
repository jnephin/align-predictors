# Name: BoPclip.py
# Created on: 2017-03-06
# Author: Jessica Nephin

# Description:
#			Clips NCC bottom patches to correct boundary
#			Converts factor attributes
#			Removes fields

# Import modules
import os
import arcpy


# move up one directory
os.chdir('..')

# allow overwriting
arcpy.env.overwriteOutput = True

# Set environment settings
arcpy.env.workspace = os.getcwd()

# Bottom patches, get layer basename
g = "NCC_BoPs_v1.1.gdb"
inLayer = "BoP18_merged"


# Input feature
inFeature = "InputData/Polygons/NCC_BoPs_v1.1.gdb/BoP18_merged"
# Boundary layer
boundary = os.getcwd()+"/Boundary/NCC_Nearshore_Area_BoP.shp"
#Output feature
outFeature = "InputData/Polygons/NCC_BoPs_v1.1.gdb/BoP_clipped"

# Clip layer
arcpy.Clip_analysis(inFeature, boundary, outFeature)


#-----------------------------------------------------------#
# Combine Btype1 and Btype2

# Add field
fexists = arcpy.ListFields (outFeature, "BTypeComb")
if len(fexists) != 1:
	arcpy.AddField_management (outFeature, "BTypeComb", "TEXT")
#Calculate field
arcpy.CalculateField_management (outFeature, "BTypeComb", "!BType1! + !BType2!", "PYTHON_9.3")


#-----------------------------------------------------------#
# Convert attributes to integer factors

# BType

# Add field
fexists = arcpy.ListFields (outFeature, "BType")
if len(fexists) != 1:
	arcpy.AddField_management (outFeature, "BType", "SHORT")
#Calculate field
arcpy.CalculateField_management (outFeature, "BType",
								'''{"1": "1", "1a": "2", "1b": "3",
								"2": "4", "2a": "5", "2b": "6",
								"3": "7", "3a": "8", "3b": "9"}.get(!BTypeComb!, "0")''',
								"PYTHON_9.3")

# DepthCode

# Add field
fexists = arcpy.ListFields (outFeature, "DepthBin")
if len(fexists) != 1:
	arcpy.AddField_management (outFeature, "DepthBin", "SHORT")
#Calculate field
arcpy.CalculateField_management (outFeature, "DepthBin",
								'''{"ITD": "1", "0to5": "2", "5to10": "3",
								"10to20": "4", "20to50": "5"}.get(!DepthCode!, "0")''',
								"PYTHON_9.3")

#-----------------------------------------------------------#
# Remove feilds

# add new feature
finalFeature = "InputData/Polygons/NCC_BoPs_v1.1.gdb/BoP"
arcpy.CopyFeatures_management(outFeature, finalFeature)

arcpy.DeleteField_management (finalFeature, ["SourceKey", "Confidence",
						"ObsBType1", "ObsBType2", "ObsArea","ObsDist", "GrabBType1",
						"GrabBType2", "GrabArea", "GrabDist", "SZBType1","SZBType2",
						"SZArea","SZITDDist", "SZ0to5Dist", "ObsDepthCode", "FragmentOrigFID",
						"GrabDepthCode","GrabSourceKey", "SZDepthCode","SZSourceKey",
						"ObsSourceKey", "BType1", "BType2", "BTypeComb", "DepthCode"])
