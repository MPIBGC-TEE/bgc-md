# Notes:
# For multiyear runs the output of out_cable.nc
# has to be renamed (by giving the year in the filename) after every year to prevent the postprocessing script from overiding it
# It should be possible to get this out of the namelist file
# To run cable for many years you have to restart it again 
# For the original look at the file:
# My Passport/cable_chris_transit_time/CABLE-run-test-lqy/spinup/run_spinup 
# For the cable run as Chris did for the transit time papers we use the  script mknml.bash in cable_chris_transit_time/mm/ on PASSPORT
# we have to change the paths in this scripts
# instead of /data/lo02b/CABLE-run-tracebility we need  My_Passport/cable_chris_transit_time/CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised
# veg_params_cable_MK3L_v2_kf.txt
# 
# age4_annual.ncl produces fluxes (in this script tha last of before years values are used (364,:,:,:) since they are updated later or eqrlier than other varibles
# see also the pseudo code in  GetFluxFromCABLEoutput.txt in PASSPort/cable_chris_transit_time/CABLE-transit-time-real/archive_TransitTime/scripts (array dimensions do not always match there)
# - in ncl 0 means first index (like python)

