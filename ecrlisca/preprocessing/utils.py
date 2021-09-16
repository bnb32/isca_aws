import ecrlisca.environment
from ecrlisca.data.co2 import series as co2series
from ecrlisca.experiment import Experiment
import os
import netCDF4 as nc
import numpy as np
import glob
import xarray as xr
import xesmf as xe
import warnings
warnings.filterwarnings("ignore")

land_years = glob.glob(os.environ.get("RAW_TOPO_DIR")+'/Map*.nc')
land_years = sorted([l.strip('Ma.nc').split('_')[-1] for l in land_years],key=lambda x:float(x))

def solar_constant(land_year):
    #assuming years prior to current era is expressed as a positive value
    time = -float(land_year)/4700.0
    return 1370.0/(1-0.4*time)

def interp(a,b,dt):
    return a*(1-dt)+dt*b

def interpolate_co2(land_year):

    year = float(land_year)

    keys = sorted(co2series)
    kf = [float(k) for k in keys]

    if land_year in keys:
        return co2series[land_year]

    if year <= kf[0]:
        return co2series[keys[0]]

    if year >= kf[-1]:
        return co2series[keys[-1]]

    for i in range(len(keys)):
        if kf[i] <= year <= kf[i+1]:
            return interp(co2series[keys[i]],
                          co2series[keys[i+1]],
                          (year-kf[i])/(kf[i+1]-kf[i]))

def adjust_co2(multiplier=1,land_year=0,co2_value=None,outfile=None):
    
    ecrlexp = Experiment(multiplier=multiplier,land_year=land_year,co2_value=co2_value)

    base_dir = os.path.dirname(os.path.realpath(__file__))
    co2_path = os.environ.get('RAW_CO2_DIR')
    input_dir = os.environ.get('CO2_DIR')
    new_file = os.path.join(input_dir,f'{ecrlexp.co2_file}')

    os.system(f'mkdir -p {input_dir}')
    os.system(f'rm -f {new_file}')
    os.system(f'cp {co2_path}/co2.nc {new_file}')
    filename = new_file
    ncfile = nc.Dataset(filename,'r+')
    co2 = ncfile.variables['co2']
        
    if co2_value is None:    
        co2[:,:,:,:] = float(multiplier)*interpolate_co2(land_year)
    else:    
        co2[:,:,:,:] = float(co2_value)

    ncfile.variables['co2'][:,:,:,:] = co2[:,:,:,:]
    ncfile.close()

def adjust_continents(land_year=0,sea_level=0):
    land = interpolate_land(land_year)
    regrid_continent_data(land,land_year=land_year)

def regrid_continent_data(land,land_year=0):

    base = xr.open_mfdataset(os.environ.get('BASE_TOPO_FILE'))

    ds_out = xr.Dataset({'lat': (['lat'], base['lat'].values),
                         'lon': (['lon'], base['lon'].values)})

    out_file = os.path.join(os.environ.get('TOPO_DIR'),Experiment(land_year=land_year).land_file)

    regridder = xe.Regridder(land, ds_out, 'bilinear')
    tmp = land['z'].values
    tmp[tmp<sea_level] = 0
    #ds_out['z'].values[ds_out['z'].values < 0] = 0
    land['z'] = (land['z'].dims,tmp)
    ds_out = regridder(land)
    ds_out['land_mask'] = (ds_out['z'].dims,np.array(ds_out['z'].values > 0.0,dtype=float))
    ds_out = ds_out.rename({'z':'zsurf'})
    ds_out = ds_out.fillna(0)
    os.system(f'rm -f {out_file}')
    ds_out.to_netcdf(out_file)
    print(f'{out_file}')
    return ds_out

def interpolate_land(land_year):
    year = float(land_year)

    keys = sorted(land_years)
    kf = [float(k) for k in keys]

    if land_year in keys:
        return get_original_map_data(land_year)

    if year <= kf[0]:
        return get_original_map(keys[0])

    if year >= kf[-1]:
        return get_original_map(keys[-1])

    for i in range(len(keys)):
        if kf[i] <= year <= kf[i+1]:
            ds_out = get_original_map_data(keys[i])
            tmp = interp(get_original_map_data(keys[i])['z'].values,
                         get_original_map_data(keys[i+1])['z'].values,
                         (year-kf[i])/(kf[i+1]-kf[i]))
            ds_out['z'] = (ds_out['z'].dims,tmp)
            return ds_out

def get_original_map_data(land_year):
    land_year = str(land_year)
    file = glob.glob(os.environ.get("RAW_TOPO_DIR")+f'/Map*_{land_year}Ma.nc')
    land = xr.open_mfdataset(file)
    return land

def regrid_continent_maps(remap_file):

    land_year = f'{remap_file.strip(".nc").split("_")[-1]}'
    land = xr.open_mfdataset(remap_file)
    
    regrid_continent_data(land,land_year)
