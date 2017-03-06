# Name: MaskConvert.R
# Created on: 2016-12-22
# Edited on: 2017-01-26
# Author: Jessica Nephin


# Masks input raster using clipped to coastline BoP layer
# Exports raster with appropriate data type to limit storage space

# required packages
require(parallel)

# working directory
setwd('..')


####----------------------------------------------------------------------####
## Function

## Masks env.layers and exports tiff with chosen datatype
maskconv <- function(rasterfile, datatype){
  # packages
  require(raster)
  require(rgdal)

  # infile
  inf = paste0("InputData/Rasters/Resampled/", rasterfile)
  # outfile
  outf = paste0("AlignedData/Rasters/", rasterfile)

  # run if file exists
  if(file.exists(inf)){

    # load input raster
    ras <- raster(inf)
    # load masked BoP rasted
    bopmask <- raster("AlignedData/Rasters/BType.tif")

    # set ful proj string
    proj4string(ras) <- proj
    proj4string(bopmask) <- proj

    # BoP extents
    ext <- extent(bopmask)

    # Crop - crop raster to spatial extent of bop raster
    tmp <- paste0("InputData/Rasters/",rasterfile,"_tmp.tif")
    cras <- raster::crop(ras, ext, filename=tmp, overwrite=TRUE, format = "GTiff", datatype = datatype)

    # Mask - converts cells in raster to NA where cells are == NA in bop
    mras <- raster::mask(cras, bopmask, filename=outf, overwrite=TRUE, format = "GTiff", datatype = datatype)

    # clean up tmp files
    unlink(tmp)
  }
}




####----------------------------------------------------------------------####
# Variables

#full bc albers proj
proj <- "+proj=aea +lat_1=50 +lat_2=58.5 +lat_0=45 +lon_0=-126 +x_0=1000000 +y_0=0 +datum=NAD83 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"

## List  rasters
rasters <- list.files(path="InputData/Rasters/Resampled",pattern=".tif$")



####----------------------------------------------------------------------####
# Run maskconv()

## create cluster object
num_cores <- detectCores() - 1
cl <- makeCluster(num_cores)

## make variables and packages available to cluster
clusterExport(cl, varlist="proj")

# apply function over clusters for thiessen interp layers
parSapply(cl, rasters, FUN=maskconv, datatype="FLT4S")

## stop cluster
stopCluster(cl)
