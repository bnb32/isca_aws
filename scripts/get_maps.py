import xarray as xr
import numpy as np
import xesmf as xe
import sys
import ecrlisca.environment
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
data_dest = os.path.join(os.environ.get('ISCA_REPO_DIR'),'experiments/input/land_masks')
cmd = f'cd {data_dest}; wget {data_source}; '
cmd += f'unzip {os.path.join(data_dest,zip_file)}'

if args.download:
    os.system(cmd)

def regrid_continent_maps(remap_file):

    base_file = os.path.join(os.environ.get('GFDL_BASE'),'input/land_masks/era_land_t42.nc')
    base = xr.open_mfdataset(base_file)

    ds_out = xr.Dataset({'lat': (['lat'], base['lat'].values),
                         'lon': (['lon'], base['lon'].values)})


    out_file = f'continents_{remap_file.split("_")[-1]}'

    out_dir = os.path.join(os.environ.get('ISCA_REPO_DIR'),'experiments/input/land_masks')
    out_file = os.path.join(out_dir,out_file)

    land = xr.open_mfdataset(remap_file)
    regridder = xe.Regridder(land, ds_out, 'bilinear')
    ds_out = regridder(land)
    tmp = np.zeros(ds_out['z'].values.shape)
    tmp = ds_out['z'].values
    tmp[tmp<0] = 0
    #ds_out['z'].values[ds_out['z'].values < 0] = 0
    ds_out['z'] = (ds_out.dims,tmp)
    ds_out['land_mask'] = (ds_out.dims,np.array(ds_out['z'].values > 0.0,dtype=float))
    ds_out = ds_out.rename({'z':'zsurf'})
    ds_out = ds_out.fillna(0)
    os.system(f'rm -f {out_file}')
    ds_out.to_netcdf(out_file)
    print(f'{out_file}')


def get_original_map_file(land_year):
    file = glob.glob(f'{data_dest}/{zip_file.strip(".zip")}*/Map*_{land_year}Ma.nc')
    return file

files = glob.glob(f'{data_dest}/{zip_file.strip(".zip")}*/Map*.nc')



if args.regrid:
    for f in files:
        regrid_continent_maps(f)    
