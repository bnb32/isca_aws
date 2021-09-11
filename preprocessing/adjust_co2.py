import sys
sys.path.insert(0,'../')
import environment
import os
import netCDF4 as nc
import numpy as np
import argparse

parser=argparse.ArgumentParser(description="Adjust CO2")
parser.add_argument('-multiplier', default=2.0)
args=parser.parse_args()

base_dir = os.path.dirname(os.path.realpath(__file__))
co2_path = os.path.join(os.environ.get('GFDL_BASE'),'exp/test_cases/variable_co2_concentration/input/')
input_dir = os.path.join(base_dir,f'../experiments/input/')
new_file = os.path.join(input_dir,f'co2_{args.multiplier}x.nc')

os.system(f'mkdir -p {input_dir}')
os.system(f'rm -f {new_file}')
os.system(f'cp {co2_path}/co2.nc {new_file}')
filename = new_file
ncfile = nc.Dataset(filename,'r+')
co2 = ncfile.variables['co2']
co2[:,:,:,:] = float(args.multiplier)*co2[:,:,:,:]
ncfile.variables['co2'][:,:,:,:] = co2[:,:,:,:]
ncfile.close()
