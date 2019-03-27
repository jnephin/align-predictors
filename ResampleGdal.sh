# Name: ResampleGdal.sh
# Created on: 2017-01-26
# Edited on: 2018-04-30
# Author: Jessica Nephin

## Resample raster environmental layers to align with NCC BoP 20m raster

# spatial extent of NCC BoP 20 x 20 m raster
# xmin=670704.183
# xmax=954444.183
# ymin=689856.440
# ymax=1221076.440

# spatial extent of NSB_SSB
# xmin=459940.032
# xmax=1298440.032
# ymin=327690.883
# ymax=1227390.883

# run from parent folder
# cd to directory directory
cd Data/NCC_nearshore/InputData/Raster/

# loop through layers to resample
for i in $(ls Original/*range.tif); do

    # get basename
    basext=${i##*/}
    base=${basext%.*}

    # input, output
    in=$i
    out="Resampled/${base}.tif"

    # spatial extents of BoP raster - aligns all raster (origin and res) for SDM
    xmin=670704.183
    xmax=954444.183
    ymin=689856.440
    ymax=1221076.440

    #run gdalwarp bilinear resample at cell size (-tr option)
    gdalwarp --config GDAL_CACHEMAX 500 -wm 3000 -multi -r bilinear -ot Float32 -tr 20 20 -overwrite -te $xmin $ymin $xmax $ymax $in $out

done
