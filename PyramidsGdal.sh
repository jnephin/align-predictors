## build pyramids and calculate stats

cd Data/NCC_nearshore/AlignedData/Raster

#  add stats and pyramids
for r in $(ls *.tif); do
   gdalinfo -stats $r
   gdaladdo -r nearest $r 2 4 8 16
done
