# Name: ResampleGdal.sh
# Created on: 2017-01-26
# Edited on: 2017-01-26
# Author: Jessica Nephin

## Resample raster environmental layers to align with NCC BoP 20m raster

# spatial extent of NCC BoP 20 x 20 m raster
# xmin=664130.7863 ymin=685234.285 xmax=954450.7863 ymax=1221814.285
# Origin = (664130.786299999800000,1221814.285000000100000)

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
    xmin=664130.7863
    ymin=685234.285
    xmax=954450.7863
    ymax=1221814.285

	#run gdalwarp cubic spline resample at 20 x 20 m cell size
    gdalwarp --config GDAL_CACHEMAX 500 -wm 3000 -multi -r bilinear -ot Float32 -tr 20 20 -overwrite -te $xmin $ymin $xmax $ymax $in $out

done
