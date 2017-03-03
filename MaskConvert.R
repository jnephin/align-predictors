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
# Mask BoP my NCC area (only run this once)
require(raster)
require(rgdal)
# load unclipped BoP raster
bop <- raster("InputData/Rasters/BoP_Aligned/BType.tif")
# load NCC mask
ncc <- readOGR(dsn = "Boundary", layer = "NCC_Nearshore_Area_BoP")
# Mask - assigns NA values outside of region polygon
out <- "AlignedData/Rasters/BType.tif"
rasterize(ncc, bop, mask=TRUE, filename=out, overwrite=TRUE, format = "GTiff", datatype = "INT1U")




####----------------------------------------------------------------------####
## Function

## Masks env.layers and exports tiff with chosen datatype
maskconv <- function(rasterfile, datatype){
  # packages
  require(raster)
  require(rgdal)

  # infile
  inf = paste0("InputData/Rasters/BoP_Aligned/", rasterfile, ".tif")
  # outfile
  outf = paste0("AlignedData/Rasters/", rasterfile, ".tif")

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
    tmp <- paste0("InputData/Rasters/BoP_Aligned/",rasterfile,"_tmp.tif")
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

## List of numeric rasters
rastersnum <- c("Chla_mean","distLand","FBPI","fetchMax","fetchMean","fetchNW","fetchSE","MBPI",
                "rng_MaxSp","rng_MnSp","rng_Sal","rng_Stress","rng_Temp","Slope","spr_MaxSp",
                "spr_MnSp","spr_Sal","spr_Stres","spr_Temp","ArcRug","bathy","BBPI")

## List of INT1U integer rasters
rasters1int <- c("Bloom_Freq","DepthCode")




####----------------------------------------------------------------------####
# Run maskconv()

## create cluster object
num_cores <- detectCores() - 1
cl <- makeCluster(num_cores)

## make variables and packages available to cluster
clusterExport(cl, varlist="proj")

# apply function over clusters for thiessen interp layers
parSapply(cl, rastersnum, FUN=maskconv, datatype="FLT4S")
parSapply(cl, rasters1int, FUN=maskconv, datatype="INT1U")

## stop cluster
stopCluster(cl)
