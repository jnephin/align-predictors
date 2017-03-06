# Name: ResampleGdal.sh
# Created on: 2017-01-26
# Edited on: 2017-01-26
# Author: Jessica Nephin

## Resample raster environmental layers to align with NCC BoP 20m raster

# spatial extent of NCC BoP 20 x 20 m raster
# xmin=670704.183 ymin=689856.440 xmax=954444.183 ymax=1221076.440
# Origin = (670704.183299999680000,1221076.439799999800000)
# Center  =   (  812574.183,  955466.440)

# move to working directory
cd ..
cd Inputdata/Rasters

# loop through layers to resample
for i in $(ls Original/*.tif); do

    # get basename
    basext=${i##*/}
    base=${basext%.*}

    # input, output
    in=$i
    out="Resampled/${base}.tif"

	# spatial extents of BoP raster - aligns all raster (origin and res) for SDM
    xmin=670704.183
    ymin=689856.440
    xmax=954444.183
    ymax=1221076.440

	#run gdalwarp cubic spline resample at 20 x 20 m cell size
    gdalwarp --config GDAL_CACHEMAX 500 -wm 3000 -multi -r bilinear -ot Float32 -tr 20 20 -overwrite -te $xmin $ymin $xmax $ymax $in $out

done
