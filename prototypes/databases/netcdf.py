import netCDF4
import numpy as np
import matplotlib.pyplot as plt
f= netCDF4.Dataset('/home/mm/bgc-md/orders/2f5c607344a3b964484cefd6c9ccf0ca/NACP_MSTMIP_MODEL_DRIVER/data/mstmip_driver_global_hd_climate_tair_monthly_mean_1901_v1.nc4')
print(f)
lat=f.variables['lat']
lon=f.variables['lon']
latvals = lat[:]; lonvals = lon[:] 
# a function to find the index of the point closest pt
# (in squared distance) to give lat/lon value.
def getclosest_ij(lats,lons,latpt,lonpt):
    # find squared distance of every point on grid
    dist_sq = (lats-latpt)**2 + (lons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, lats.shape)
LAT,LON=np.meshgrid(lat,lon)

iy_min, ix_min = getclosest_ij(LAT, LON, 180+2*50,(180+11)*2)
