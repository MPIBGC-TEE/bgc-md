set -e
odir="output/new4"
yr=1910
cat <<EOF >fcnpspin.lst
10
${odir}/cnpspindump1901.nc
${odir}/cnpspindump1902.nc
${odir}/cnpspindump1903.nc
${odir}/cnpspindump1904.nc
${odir}/cnpspindump1905.nc
${odir}/cnpspindump1906.nc
${odir}/cnpspindump1907.nc
${odir}/cnpspindump1908.nc
${odir}/cnpspindump1909.nc
${odir}/cnpspindump1910.nc
EOF

cp -p cable_CN_spincasa_${yr}.nml cable.nml
mpirun -np 9 --oversubscribe ../../CABLE-SRC/offline/tmpParallel/cable-mpi
mv out_cable.nc     ${odir}/out_ncar_${i}_0_ndep.nc
cp -p restart_out.nc restart_in.nc
cp -p poolcnp_out.csv poolcnp_in.csv
mv restart_out.nc ${odir}/restart_ncar_${yr}_ndep.nc
mv poolcnp_out.csv ${odir}/poolcnp_out_${yr}_ndep.csv


