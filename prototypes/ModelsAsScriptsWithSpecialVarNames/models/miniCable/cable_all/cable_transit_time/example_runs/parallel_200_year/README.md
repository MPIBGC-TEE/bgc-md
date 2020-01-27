# Notes:
# - after every year the output of out_cable.nc
#   has to be renamed (given the year in the filename) to prevent the postprocessing script from overiding it
#   It should be possible to get this out of the namelist file
# - To run cable for many years you have to restart it again look at the file
#   CABLE-run-test.lgy/spinup (on the harddrive)
#   for the cable run as Chris did we use the  script mknml.bash in cable_chris_transit_time/mm/ on PASSPORT
# we have to change the paths in this scripts
# instead of /data/lo02b/CABLE-run-tracebility we need 
# ../../CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised
# (originally # My_Passport/cable_chris_transit_time/CABLE-AUX/offline/gridinfo_NCAR_1.9x2.5_landfrac_revised
#
# veg_params_cable_MK3L_v2_kf.txt
# 
# age4_annual.ncl produces fluxes (in this script tha last of before years values are used (364,:,:,:) since they are updated later or eqrlier than other varibles
# see also the pseudo code in  GetFluxFromCABLEoutput.txt in PASSPort/cable_chris_transit_time/CABLE-transit-time-real/archive_TransitTime/scripts (array dimensions do not always match there)
# - in ncl 0 means first index (like python)

