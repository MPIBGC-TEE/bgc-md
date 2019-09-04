#! see ../README about how to run cable in general for several years
# Here we try to reproduce exactly the conditions that produced the data of the paper

# First we run the spinup 
# To be able to do that we have to produce the nml files for each year
# the original in in My Passport/cable_chris_transit_time/nml/mknml.bash
# I changed the paths to the AUX dir 
# this will produce a bunch of *.nml files

# now we run the adapted spinup script
./runspinup_mm.sh #sometimes the spinup has to be increase. Use Jianyang Xia 's method to compute 
cp ../spinup/restart_in.nc .
cp ../spinup/poolcnp_in.csv .

yr=1901
  while [ $yr -le 2100 ]
  do
    #mm the files are now produced here
    #cp -p /home/599/czl599/nml/cable_C_spinup_${yr}.nml cable.nml
    cp -p cable_CN_VCO2VMet_${yr}.nml cable.nml #for the paper only CN S1
#    cp -p cable_CN_CCO2VMet_${yr}.nml cable.nml #for the paper only CN S2
#    cp -p cable_CN_VCO2CMet_${yr}.nml cable.nml #for the paper only CN S3
    # mm: I cant find this file:
    # assuming My\ Passport/cable_chris_transit_time/
    mpirun -np 9 --oversubscribe ../../CABLE-SRC/offline/tmpParallel/cable-mpi
    mv out_cable.nc      output/new4/out_ncar_${yr}_ndep.nc
    mv log_cable.txt     output/new4/log_ncar_${yr}_ndep.txt
    cp -p restart_out.nc restart_in.nc
    cp -p poolcnp_out.csv poolcnp_in.csv
    mv cnpflux${yr}.csv  output/new4/cnpfluxndep_${yr}_ndep.csv
    mv restart_out.nc    output/new4/restart_ncar_${yr}_ndep.nc
    mv poolcnp_out.csv   output/new4/poolcnp_out_${yr}_ndep.csv
    yr=`expr $yr + 1`
  done
  i=`expr $i + 1`
done
