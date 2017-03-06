# EnvLayers2BoP.py
# Created on: 2016-12-16
# Edited on: 2017-01-26
# Author: Jessica Nephin
#
# Description: Overlay environmental polygons with BoPs in order to get
#			   an area-weighted mean of env. polygons from point origin (A)
#              and from raster origin (B) on bottom patches.
#
# Steps:
# 1. Overlay Thiessen Polygons with BoP using 'identity'
# 2. Assign zero value to overlay shape area where env. layers do not
#    overlap BoP
# 3. Recalculate BoP shape area to exclude the area where env. layers do not
#    overlap BoP
# 4. Divide updated overlay shape area with updated BoP shape area to get
#    proportion of area for weighted mean
# 5. Calculate env. variable area weighted mean for each BoP polygon

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#

# Import modules
import os
import arcpy

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Create envrionmental variables
arcpy.env.overwriteOutput = True

# move up one directory
os.chdir('..')

# Get workspace
arcpy.env.workspace =  os.getcwd()
inpath = "InputData/Polygons"
outpath = "AlignedData/Polygons"

# BoP geodatabases and paths
bop = os.path.join(os.getcwd(),inpath,"NCC_BoPs_v1.1.gdb/BoP")
gdbpath = os.path.join(os.getcwd(),outpath)
BoPenv = os.path.join(os.getcwd(),outpath,"BoP_Env.gdb/BoP")

# Create Env BoP geodatabase if it doesn't already exist
exists = arcpy.Exists(os.path.join(gdbpath,"BoP_Env.gdb"))
if(not exists):
	arcpy.CreateFileGDB_management (gdbpath, "BoP_Env.gdb")

	# Copy BoP to new Env BoP geodatabase
	arcpy.CopyFeatures_management(bop, os.path.join(gdbpath,"BoP_Env.gdb/BoP"))


#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#

# A) Loop through point origin envrionmental data geodatabases
gdb = ["Currents.gdb","Fetch.gdb","SalTemp.gdb"]
for g in gdb:

	# Get Environmental variable name
	desc = arcpy.Describe(inpath+'/'+g)
	evname = desc.baseName

	# layers
	env = os.path.join(inpath,g,evname+"_Interp")
	env_BoP = os.path.join(inpath,g,evname+"_BoPoverlay")
	uptable = os.path.join(inpath,g,evname+"_table")
	boptable = os.path.join(inpath,g,evname+"_BoPtable")


	# 1)
	# Overlay Env with BoP
	arcpy.Identity_analysis (bop, env, env_BoP)

	# 2)
	# Create a copy of shape area called Update_Area to be edited
	fexists = arcpy.ListFields (env_BoP, "Update_Area")
	if len(fexists) != 1:
		arcpy.AddField_management (env_BoP, "Update_Area", "DOUBLE", 18, 11)
	arcpy.CalculateField_management (env_BoP, "Update_Area", "!Shape_Area!", "PYTHON_9.3")

	#  Assign update area value to zero where env. layer does not overlap BoP
	selfield = "FID_"+evname+"_Interp"
	with arcpy.da.UpdateCursor (env_BoP, ["Update_Area", "OBJECTID"], selfield +  "= -1") as cursor:
		for update, key in cursor:
			#create row
			row = (0, key)
			#update row
			cursor.updateRow (row)

	del cursor

	#3)
	# Calculate sum of Update_Area per BoP
	arcpy.Statistics_analysis(env_BoP, uptable,  [["Update_Area", "SUM"]], "BoPID")

	# Create dictionary for BoPID and SUM of update area
	valueDi = dict ([(key, val) for key, val in
					 arcpy.da.SearchCursor
					 (uptable, ["BoPID", "SUM_Update_Area"])])

	# Update env_BoP polygons with Sum_Area
	fexists = arcpy.ListFields (env_BoP, "Sum_Area")
	if len(fexists) != 1:
		arcpy.AddField_management(env_BoP, "Sum_Area", "DOUBLE", 18, 11)

	with arcpy.da.UpdateCursor (env_BoP, ["Sum_Area", "BoPID"]) as cursor:
		for update, key in cursor:
			#create row
			row = (valueDi [key], key)
			#update row
			cursor.updateRow (row)

	del cursor

	# 4)
	# Add Field: divide overlay area by BoP area
	fexists = arcpy.ListFields (env_BoP, "Prop_Area")
	if len(fexists) != 1:
		arcpy.AddField_management (env_BoP, "Prop_Area", "DOUBLE", 18, 11)
	arcpy.CalculateField_management (env_BoP, "Prop_Area", "!Update_Area! / !Sum_Area!", "PYTHON_9.3")

	# Set fields
	if evname == "SalTemp":
		fields = ["spr_Sal","rng_Sal","spr_Temp","rng_Temp"]
	elif evname == "Fetch":
		fields = ["fetchNW","fetchSE","fetchMax","fetchMean","distLand"]
	elif evname == "Currents":
		fields = ["spr_MnSp","rng_MnSp","spr_MaxSp","rng_MaxSp","spr_Stres","rng_Stress"]

	# 5)
	# Loop through fields to add to BoP
	for f in fields:

		# Add Field: multiply proportion of area by env. value (for each ev. field)
		newfield = f+"_aw"
		fexists = arcpy.ListFields(env_BoP, newfield)
		if len(fexists) != 1:
			arcpy.AddField_management (env_BoP, newfield, "DOUBLE", 18, 11)
		arcpy.CalculateField_management (env_BoP, newfield,  '!' + f + '! * !Prop_Area!', "PYTHON_9.3")

		# Summary statistics: sum area weighted env. values for each BoP
		arcpy.Statistics_analysis (env_BoP, boptable,  [[newfield, "SUM"]], "BoPID")
		# update field name
		fname = arcpy.ListFields(boptable)[3].name
		arcpy.AlterField_management(boptable, fname, f, f)

		# Add new field to BoP to be updated
		fexists = arcpy.ListFields(BoPenv, f)
		if len(fexists) != 1:
			arcpy.AddField_management (BoPenv, f, "DOUBLE", 18, 11)

		# Join env field to BoP attribute table using dictionary and update cursor
		# Value: field with value to be transferred
		valueDi = dict ([(key, val) for key, val in
						 arcpy.da.SearchCursor
						 (boptable, ["BoPID", f])])

		# Update feature class
		with arcpy.da.UpdateCursor (BoPenv, [f, "BoPID"]) as cursor:
			for update, key in cursor:
				#skip if key value is not in dictionary
				if not key in valueDi:
					continue
				#create row
				row = (valueDi [key], key)
				#update row
				cursor.updateRow (row)

		del cursor



#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#

# B) Loop through raster origin envrionmental data (raster origin)
gdb = ["Chla.gdb",] #"Bathy.gdb"]
for g in gdb:

	# Get Environmental variable name
	desc = arcpy.Describe(inpath+'/'+g)
	evname = desc.baseName

	# get gdb layers
	if evname == "Bathy":
		layer = ["ArcRug","bathy","BBPI","MBPI","FBPI","Slope"]
	elif evname == "Chla":
		layer = ["Chla_mean","Bloom_Freq"]

	# loop through gdb layers
	for l in layer:

		# layers to create
		env = os.path.join(inpath,g,l)
		env_BoP = os.path.join(inpath,g,l+"_BoPoverlay")
		uptable = os.path.join(inpath,g,l+"_table")
		boptable = os.path.join(inpath,g,l+"_BoPtable")


		# 1)
		# Overlay Env with BoP
		arcpy.Identity_analysis (bop, env, env_BoP)

		# 2)
		# Create a copy of shape area called Update_Area to be edited
		fexists = arcpy.ListFields (env_BoP, "Update_Area")
		if len(fexists) != 1:
			arcpy.AddField_management (env_BoP, "Update_Area", "DOUBLE", 18, 11)
		arcpy.CalculateField_management (env_BoP, "Update_Area", "!Shape_Area!", "PYTHON_9.3")

		#  Assign update area value to zero where env. layer does not overlap BoP
		selfield = "FID_"+l
		with arcpy.da.UpdateCursor (env_BoP, ["Update_Area", "OBJECTID"], selfield +  "= -1") as cursor:
			for update, key in cursor:
				#create row
				row = (0, key)
				#update row
				cursor.updateRow (row)

		del cursor

		#3)
		# Calculate sum of Update_Area per BoP
		arcpy.Statistics_analysis(env_BoP, uptable,  [["Update_Area", "SUM"]], "BoPID")

		# Create dictionary for BoPID and SUM of update area
		valueDi = dict ([(key, val) for key, val in
						 arcpy.da.SearchCursor
						 (uptable, ["BoPID", "SUM_Update_Area"])])

		# Update env_BoP polygons with Sum_Area
		fexists = arcpy.ListFields (env_BoP, "Sum_Area")
		if len(fexists) != 1:
			arcpy.AddField_management(env_BoP, "Sum_Area", "DOUBLE", 18, 11)

		with arcpy.da.UpdateCursor (env_BoP, ["Sum_Area", "BoPID"]) as cursor:
			for update, key in cursor:
				#create row
				row = (valueDi [key], key)
				#update row
				cursor.updateRow (row)

		del cursor

		# 4)
		# Add Field: divide overlay area by BoP area
		fexists = arcpy.ListFields (env_BoP, "Prop_Area")
		if len(fexists) != 1:
			arcpy.AddField_management (env_BoP, "Prop_Area", "DOUBLE", 18, 11)
		arcpy.CalculateField_management (env_BoP, "Prop_Area", "!Update_Area! / !Sum_Area!", "PYTHON_9.3")


		# 5)
		# Add Field: multiply proportion of area by env. value (for each ev. field)
		newfield = l+"_aw"
		fexists = arcpy.ListFields(env_BoP, newfield)
		if len(fexists) != 1:
			arcpy.AddField_management (env_BoP, newfield, "DOUBLE", 18, 11)
		arcpy.CalculateField_management (env_BoP, newfield,  '!' + l + '! * !Prop_Area!', "PYTHON_9.3")

		# Summary statistics: sum area weighted env. values for each BoP
		arcpy.Statistics_analysis (env_BoP, boptable,  [[newfield, "SUM"]], "BoPID")
		# update field name
		lname = arcpy.ListFields(boptable)[3].name
		arcpy.AlterField_management(boptable, lname, l, l)

		# Add new field to BoP to be updated
		fexists = arcpy.ListFields(BoPenv, l)
		if len(fexists) != 1:
			arcpy.AddField_management (BoPenv, l, "DOUBLE", 18, 11)

		# Join env field to BoP attribute table using dictionary and update cursor
		# Value: field with value to be transferred
		valueDi = dict ([(key, val) for key, val in
						 arcpy.da.SearchCursor
						 (boptable, ["BoPID", l])])

		# Update feature class
		with arcpy.da.UpdateCursor (BoPenv, [l, "BoPID"]) as cursor:
			for update, key in cursor:
				#skip if key value is not in dictionary
				if not key in valueDi:
					continue
				#create row
				row = (valueDi [key], key)
				#update row
				cursor.updateRow (row)

		del cursor
