#!/bin/bash 
set -e
source ../common_config
# see ../README about how to run cable in general for several years
# Here we try to reproduce exactly the conditions that produced the data of the paper

# First we check if the spinup has already been run or run it.
if [ ! -d "../${spinupDir}" ]; then
  ./runspinup_mm.sh #sometimes the spinup has to be increased. Use Jianyang Xia 's method to compute 
fi
cp ../${spinupDir}/restart_in.nc .
cp ../${spinupDir}/poolcnp_in.csv .
#prepare output directory
mkdir -p ${odir}

startyr=1901
endyr=2100
mknml_files $startyr $endyr
yr=$startyr
while [ $yr -le $endyr ]
do
  #mm the files are now produced here
  #cp -p /home/599/czl599/nml/cable_C_spinup_${yr}.nml cable.nml
  cp -p cable_CN_VCO2VMet_${yr}.nml cable.nml #for the paper only CN S1
  # cp -p cable_CN_CCO2VMet_${yr}.nml cable.nml #for the paper only CN S2 #this line gives a segfault while reading the Met file 
  # cp -p cable_CN_VCO2CMet_${yr}.nml cable.nml #for the paper only CN S3 #this line gives a segfault while reading the Met file 
  mpirun -np ${np} --oversubscribe ../${cable_exe}
  mv out_cable.nc      ${odir}/out_ncar_${yr}_ndep.nc
  mv log_cable.txt     ${odir}/log_ncar_${yr}_ndep.txt
  cp -p restart_out.nc restart_in.nc
  cp -p poolcnp_out.csv poolcnp_in.csv
  mv cnpflux${yr}.csv  ${odir}/cnpfluxndep_${yr}_ndep.csv
  mv restart_out.nc    ${odir}/restart_ncar_${yr}_ndep.nc
  mv poolcnp_out.csv   ${odir}/poolcnp_out_${yr}_ndep.csv
  yr=`expr $yr + 1`
done
