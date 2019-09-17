#!/bin/bash
set -e
odir="output/new4"
spinStart=1901
spinEnd=1910
runSpinupYears() {
  echo "got value i=$1"
  i_max=$1
  echo "######################################################################################################"
	echo "i=${i} of ${i_max}"
  i=1
  while [ $i -le $i_max ]
  do
  yr=$spinStart
    while [ $yr -le $spinEnd]
    do
      echo "######################################################################################################"
      echo "yr=${yr}"
      cp -p cable_CN_spiupdump_${yr}.nml cable.nml #for the paper only CN
      mpirun -np 9 --oversubscribe ../../CABLE-SRC/offline/tmpParallel/cable-mpi
      mv out_cable.nc      ${odir}/out_ncar_${i}_${yr}_ndep.nc
      mv log_cable.txt     ${odir}/log_ncar_${yr}_ndep.txt
      cp -p restart_out.nc restart_in.nc
      cp -p poolcnp_out.csv poolcnp_in.csv
      mv cnpflux${yr}.csv  ${odir}/cnpfluxndep_${yr}_ndep.csv
      mv restart_out.nc    ${odir}/restart_ncar_${i}_${yr}_ndep.nc
      mv poolcnp_out.csv   ${odir}/poolcnp_out_${i}_${yr}_ndep.csv
      if [ $i -eq $i_max];then
        cp -p cnpspindump${yr}.nc ${odir}/
      fi
      yr=`expr $yr + 1`
    done
    i=`expr $i + 1`
  done
}

cd ../spinup
./mknml_mm.bash

echo "######################################################################################################"
echo copy pool file
cp -p ../../CABLE-run-test-lqy/spinup/poolcnp_in.csv ./poolcnp_in.csv

echo "######################################################################################################"
echo copy restart file
cp -p  ../../CABLE-run-test-lqy/spinup/restart_in.nc ./restart_in.nc


#prepare directory
mkdir -p ${odir}

runSpinupYears 5
echo "######################################################################################################"
echo "after first loop"



lstFileName="fcnpspin.lst"
echo 10 > $lstFileName
for i in $(seq $spinStart $spinEnd)
do  
  echo "${odir}/cnspindump${i}.nc" >> $lstFileName
done
cp -p cable_CN_spincasa_${yr}.nml cable.nml
mpirun -np 9 --oversubscribe ../../CABLE-SRC/offline/tmpParallel/cable-mpi
mv out_cable.nc     ${odir}/out_ncar_${i}_0_ndep.nc
cp -p restart_out.nc restart_in.nc
cp -p poolcnp_out.csv poolcnp_in.csv
mv restart_out.nc ${odir}/restart_ncar_${yr}_ndep.nc
mv poolcnp_out.csv ${odir}/poolcnp_out_${yr}_ndep.csv
echo "######################################################################################################"
echo "after SASU"


runSpinupYears 10
echo "######################################################################################################"
echo "after second loop"
