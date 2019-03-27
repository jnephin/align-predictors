# Name: MaskConvert.R
# Created on: 2016-12-22
# Edited on: 2017-01-26
# Author: Jessica Nephin


# Masks input raster using clipped to coastline BoP layer
# Exports raster with appropriate data type to limit storage space

# required packages
require(parallel)

# setwd('..')

####----------------------------------------------------------------------####
## Function

## Masks env.layers and exports tiff with chosen datatype
maskconv <- function(rasterfile, datatype){
  # packages
  require(raster)
  require(rgdal)

  # infile
  inf = paste0("Data/NCC_nearshore/InputData/Raster/Resampled/", rasterfile)
  # outfile
  outf = paste0("Data/NCC_nearshore/AlignedData/Raster/", rasterfile)

  # run if file exists
  if(file.exists(inf)){

    # load input raster
    ras <- raster(inf)
    # load raster mask
    bmask <- raster("Data/NCC_nearshore/AlignedData/Raster/BType.tif")
    # load polygon mask
    # bmask <- readOGR( dsn = "Data/NCC_nearshore/Boundary", layer = "NCC_Nearshore_Area_BoP_buffer20m")
    # bmask <- readOGR( dsn = "Data/NSB_shelf/Boundary", layer = "NSB_buffer100m")

    # set ful proj string
    proj4string(ras) <- proj
    proj4string(bmask) <- proj

    # BoP extents
    ext <- extent(bmask)

    # Crop - crop raster to spatial extent of bop raster
    tmp <- paste0("Data/NCC_nearshore/InputData/Raster/",rasterfile,"_tmp.tif")
    cras <- raster::crop(ras, ext, filename=tmp, overwrite=TRUE,
        format = "GTiff", datatype = datatype)

    # Mask - converts cells in raster to NA where cells are == NA in bop
    mras <- raster::mask(cras, bmask, filename=outf, overwrite=TRUE,
        format = "GTiff", datatype = datatype)

    # clean up tmp files
    unlink(tmp)
  }
}




####----------------------------------------------------------------------####
# Variables

#full bc albers proj
proj <- "+proj=aea +lat_1=50 +lat_2=58.5 +lat_0=45 +lon_0=-126 +x_0=1000000 +y_0=0 +datum=NAD83 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"


## List  rasters
rasters <- list.files(path="Data/NCC_nearshore/InputData/Raster/Resampled",
                          pattern=".tif$")
rasters <- c("Substrate_20m.tif")



####----------------------------------------------------------------------####
# Run maskconv()

## create cluster object
num_cores <- detectCores() - 1
cl <- makeCluster(num_cores)

## make variables and packages available to cluster
clusterExport(cl, varlist="proj")

# apply function over clusters for thiessen interp layers
#parSapply(cl, rasters, FUN=maskconv, datatype="FLT4S")
parSapply(cl, rasters, FUN=maskconv, datatype="INT1U")


## stop cluster
stopCluster(cl)
