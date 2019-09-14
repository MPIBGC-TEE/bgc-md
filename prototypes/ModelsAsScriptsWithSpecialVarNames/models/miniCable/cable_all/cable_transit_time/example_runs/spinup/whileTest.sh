i=1
odir="output/new4"
while [ $i -le 5 ]
do
  echo ""
  echo "##############################"
  echo "Start inner loop i=${i}"
  echo "##############################"
  echo ""
  yr=1901
  while [ $yr -le 1910 ]
  do
    #mm the files are now produced here
    echo cable_CN_spindump_${yr}.nml #cable.nml #for the paper only CN
    #mpirun -np 9 --oversubscribe ../../CABLE-SRC/offline/tmpParallel/cable-mpi
    echo ${odir}/out_ncar_${i}_${yr}_ndep.nc
    echo ${odir}/log_ncar_${yr}_ndep.txt
    echo "cnpflux${yr}.csv  ${odir}/cnpfluxndep_${yr}_ndep.csv"
    echo ${odir}/restart_ncar_${i}_${yr}_ndep.nc
    echo ${odir}/poolcnp_out_${i}_${yr}_ndep.csv
    if [ $i -eq 5 ];then
      echo "cnpspindump${yr}.nc ${odir}/"
    fi
    yr=`expr $yr + 1`
  done
  i=`expr $i + 1`
done
