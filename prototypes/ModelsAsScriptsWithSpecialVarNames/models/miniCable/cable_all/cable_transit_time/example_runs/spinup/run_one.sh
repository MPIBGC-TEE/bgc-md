set -e
i=1
yr=1910
cp -p cable_CN_spindump_${yr}.nml cable.nml #for the paper only CN
mpirun -np 9 --oversubscribe ../../CABLE-SRC/offline/tmpParallel/cable-mpi
mv out_cable.nc      output/new4/out_ncar_${i}_${yr}_ndep.nc
mv log_cable.txt     output/new4/log_ncar_${yr}_ndep.txt
cp -p restart_out.nc restart_in.nc
cp -p poolcnp_out.csv poolcnp_in.csv
mv cnpflux${yr}.csv  output/new4/cnpfluxndep_${yr}_ndep.csv
mv restart_out.nc    output/new4/restart_ncar_${i}_${yr}_ndep.nc
mv poolcnp_out.csv   output/new4/poolcnp_out_${i}_${yr}_ndep.csv
if [ $i -eq 5 ];then
  cp -p cnpspindump${yr}.nc output/new4/
fi
