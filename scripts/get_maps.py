import xarray as xr
import numpy as np
import xesmf as xe
import sys
import ecrlisca.environment
from ecrlisca.preprocessing.utils import regrid_continent_maps 
import os
import glob
import warnings
import argparse
warnings.filterwarnings("ignore")

parser=argparse.ArgumentParser(description="Download and regrid paleo-continent maps")
parser.add_argument('-download',action='store_true')
parser.add_argument('-regrid',action='store_true')
args=parser.parse_args()

zip_file = 'Scotese_Wright_2018_Maps_1-88_1degX1deg_PaleoDEMS_nc.zip'
data_source = f'http://www.earthbyte.org/webdav/ftp/Data_Collections/Scotese_Wright_2018_PaleoDEM/{zip_file}'
cmd = f'cd {os.environ["TOPO_DIR"]}'
cmd += f'; rm -rf {os.environ["RAW_TOPO_DIR"]}'
cmd += f'; wget {data_source}'
cmd += f'; unzip {zip_file}'
cmd += f'; mv {zip_file.strip(".zip")}_v2 {os.environ["RAW_TOPO_DIR"]}'
cmd += f'; rm {zip_file}'

if args.download:
    os.system(cmd)

if args.regrid:
    for f in files:
        regrid_continent_maps(f)    
