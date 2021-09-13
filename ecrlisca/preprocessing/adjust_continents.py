import ecrlisca.environment
import os
import netCDF4 as nc
import numpy as np
import argparse

parser=argparse.ArgumentParser(description="Adjust Continents")
parser.add_argument('-land_year', default=0)
args=parser.parse_args()

base_dir = os.path.dirname(os.path.realpath(__file__))
land_path = os.path.join(os.environ.get('GFDL_BASE'),'input/land_masks/')
input_dir = os.path.join(os.environ.get('ISCA_REPO_DIR'),'experiments/input/land_masks/')
new_file = os.path.join(input_dir,f'continents_{args.land_year}.nc')

os.system(f'mkdir -p {input_dir}')
os.system(f'rm -f {new_file}')
os.system(f'cp {land_path}/era_land_t42.nc {new_file}')
filename = new_file
ncfile = nc.Dataset(filename,'r+')
ncfile.close()
