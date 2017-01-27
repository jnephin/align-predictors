## build pyramids and calculate stats

cd ..
cd AlignedData/Rasters

#  add stats and pyramids
for r in $(ls); do
   gdalinfo -stats $r
   gdaladdo -r nearest $r 2 4 8 16
done
