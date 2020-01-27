#!/bin/bash
set -e
source ../common_config

spinStart=1901
spinEnd=1910
spindumptrunk="cnpspindump"
# 
runSpinupYears() {
  echo "got value i=$1"
  i_max=$1
  echo "######################################################################################################"
	echo "i=${i} of ${i_max}"
  i=1
  while [ $i -le $i_max ]
  do
  yr=$spinStart
    while [ $yr -le ${spinEnd} ]
    do
      echo "######################################################################################################"
      echo "yr=${yr}"
      cp -p cable_CN_spindump_${yr}.nml cable.nml #for the paper only CN
      mpirun -np ${np} --oversubscribe ../${cable_exe}
      mv out_cable.nc      ${odir}/out_ncar_${i}_${yr}_ndep.nc
      mv log_cable.txt     ${odir}/log_ncar_${yr}_ndep.txt
      cp -p restart_out.nc restart_in.nc
      cp -p poolcnp_out.csv poolcnp_in.csv
      #mv cnpflux${yr}.csv  ${odir}/cnpfluxndep_${yr}_ndep.csv 
      mv cnpflux${yr}.csv  ${odir}/cnpfluxndep_${i}_${yr}_ndep.csv # added the i dep
      mv restart_out.nc    ${odir}/restart_ncar_${i}_${yr}_ndep.nc
      mv poolcnp_out.csv   ${odir}/poolcnp_out_${i}_${yr}_ndep.csv
      if [ $i -eq $i_max ];then
        cp -p ${spindumptrunk}${yr}.nc ${odir}/
      fi
      yr=`expr $yr + 1`
    done
    i=`expr $i + 1`
  done
}
step1(){
  echo "######################################################################################################"
  echo "enter step 1"
  mkdir -p ../${spinupDir}
  cd ../${spinupDir}
  cp ../../nml/rcp85_conc_kf.txt .
  # To be able to do run the spinup we have to produce the nml files for each year
  # the original in in My Passport/cable_chris_transit_time/nml/mknml.bash
  # I changed the paths to the AUX dir 
  # this will produce a bunch of *.nml files
  mknml_files $spinStart $spinEnd
  
  echo "######################################################################################################"
  echo copy pool file
  cp -p ../../CABLE-run-test-lqy/spinup/poolcnp_in.csv ./poolcnp_in.csv
  
  echo "######################################################################################################"
  echo copy restart file
  cp -p  ../../CABLE-run-test-lqy/spinup/restart_in.nc ./restart_in.nc
  
  #prepare directory
  mkdir -p ${odir}
  
  runSpinupYears $1
  echo "######################################################################################################"
  echo "after step 1"

}

step2(){
  echo "######################################################################################################"
  echo "enter step 2"
  lstFileName="fcnpspin.lst"
  echo $(( spinEnd - spinStart + 1)) > $lstFileName
  for i in $(seq $spinStart ${spinEnd})
  do  
    echo "${odir}/${spindumptrunk}${i}.nc" >> $lstFileName
  done
  cp -p cable_CN_spincasa_${spinEnd}.nml cable.nml
  mpirun -np ${np} --oversubscribe ../${cable_exe}
  mv out_cable.nc     ${odir}/out_ncar_${i}_0_ndep.nc
  cp -p restart_out.nc restart_in.nc
  cp -p poolcnp_out.csv poolcnp_in.csv
  mv restart_out.nc ${odir}/restart_ncar_${spinEnd}_ndep.nc
  mv poolcnp_out.csv ${odir}/poolcnp_out_${spinEnd}_ndep.csv
  echo "######################################################################################################"
  echo "after step2"
}

step3(){
  echo "######################################################################################################"
  echo "enter step 3"
  runSpinupYears $1
  echo "######################################################################################################"
  echo "after step3"
}
step1 5
step2
step3 10
#step1 1
#step2
#step3 1
