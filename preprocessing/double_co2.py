import sys
sys.path.insert(0,'..')
import environment as env
import os
import netCDF4 as nc
import numpy as np

co2_path = f'{env.GFDL_BASE}/exp/test_cases/variable_co2_concentration/input/'

os.system(f'rm {co2_path}/co2.nc')
os.system(f'cp {co2_path}/co2_bkup.nc {co2_path}/co2.nc')
filename = f'{co2_path}/co2.nc'
ncfile = nc.Dataset(filename,'r+')
co2 = ncfile.variables['co2']
co2[:,:,:,:] = 2.0*co2[:,:,:,:]
ncfile.variables['co2'][:,:,:,:] = co2[:,:,:,:]
ncfile.close()
