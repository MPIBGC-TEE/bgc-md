i=1
while [ $i -le 10 ]
do
yr=1901
  while [ $yr -le 1910 ]
  do
    cp -p cable_CN_spiupdump_${yr}.nml cable.nml #for the paper only CN
    mpirun -np 9 --oversubscribe ../../CABLE-SRC/offline/tmpParallel/cable-mpi
    mv out_cable.nc      ${odir}/out_ncar_${i}_${yr}_ndep.nc
    mv log_cable.txt     ${odir}/log_ncar_${yr}_ndep.txt
    cp -p restart_out.nc restart_in.nc
    cp -p poolcnp_out.csv poolcnp_in.csv
    mv cnpflux${yr}.csv  ${odir}/cnpfluxndep_${yr}_ndep.csv
    mv restart_out.nc    ${odir}/restart_ncar_${i}_${yr}_ndep.nc
    mv poolcnp_out.csv   ${odir}/poolcnp_out_${i}_${yr}_ndep.csv
    if [ $i -eq 10 ];then
      cp -p cnpspindump${yr}.nc ${odir}/
    fi
    yr=`expr $yr + 1`
  done
  i=`expr $i + 1`
done
echo "######################################################################################################"
echo "after second loop"
echo "######################################################################################################"
