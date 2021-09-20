import ecrlisca.environment
from ecrlisca.data import co2_series, ecc_series, obl_series
from ecrlisca.experiment import Experiment
from ecrlisca.misc import land_years
import os
import netCDF4 as nc
import numpy as np
import glob
import xarray as xr
import xesmf as xe
import warnings
warnings.filterwarnings("ignore")

def mila_cycle(Amin=0,Amax=0,Acurr=0,T=0,land_year=0):

    w = 2*np.pi/T
    A = (Amax-Amin)/2.0
    A0 = (Amax+Amin)/2.0
    phase = np.arcsin((Acurr-A0)/A)
    return A0 + A*np.sin(w*land_year + phase)

def eccentricity(land_year): 

    #return mila_cycle(Amin=0.005,Amax=0.057,Acurr=0.0167,T=0.092,land_year=-land_year)
    return interpolate_ecc(land_year)

def obliquity(land_year):

    #return mila_cycle(Amin=22.1,Amax=24.5,Acurr=23.4,T=0.041,land_year=-land_year)
    return interpolate_obl(land_year)

def solar_constant(land_year):
    #assuming years prior to current era is expressed as a positive value
    time = -float(land_year)/4700.0
    return 1370.0/(1-0.4*time)

def interp(a,b,dt):
    return a*(1-dt)+dt*b

def interpolate_series(land_year,series):

    year = float(land_year)

    keys = sorted(series)

    if land_year in keys:
        return series[keys[keys.index(land_year)]]

    if year <= keys[0]:
        return series[keys[0]]

    if year >= keys[-1]:
        return series[keys[-1]]

    for i in range(len(keys)):
        if keys[i] <= year <= keys[i+1]:
            return interp(series[keys[i]],
                          series[keys[i+1]],
                          (year-keys[i])/(keys[i+1]-keys[i]))

def interpolate_co2(land_year):
    return interpolate_series(land_year,co2_series)

def interpolate_ecc(land_year):
    return interpolate_series(land_year,ecc_series)

def interpolate_obl(land_year):
    return interpolate_series(land_year,obl_series)

def adjust_co2(multiplier=1,land_year=0,co2_value=None,outfile=None):
    
    ecrlexp = Experiment(multiplier=multiplier,land_year=land_year,co2_value=co2_value)

    base_dir = os.path.dirname(os.path.realpath(__file__))
    co2_path = os.environ['RAW_CO2_DIR']
    input_dir = os.environ['CO2_DIR']
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
    return regrid_continent_data(land,land_year=land_year,sea_level=sea_level)

def regrid_continent_data(land,land_year=0,sea_level=0):

    base = xr.open_mfdataset(os.environ['BASE_TOPO_FILE'])

    ds_out = xr.Dataset({'lat': (['lat'], base['lat'].values),
                         'lon': (['lon'], base['lon'].values)})

    out_file = os.path.join(os.environ['TOPO_DIR'],Experiment(land_year=land_year).land_file)

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

    if land_year in keys:
        return get_original_map_data(keys[keys.index(land_year)])

    if year <= keys[0]:
        return get_original_map_data(keys[0])

    if year >= keys[-1]:
        return get_original_map_data(keys[-1])

    for i in range(len(keys)):
        if keys[i] <= year <= keys[i+1]:
            ds_out = get_original_map_data(keys[i])
            tmp = interp(get_original_map_data(keys[i])['z'].values,
                         get_original_map_data(keys[i+1])['z'].values,
                         (year-keys[i])/(keys[i+1]-keys[i]))
            ds_out['z'] = (ds_out['z'].dims,tmp)
            return ds_out

def get_original_map_data(land_year):
    land_year = str(land_year)
    file = glob.glob(os.environ["RAW_TOPO_DIR"]+f'/Map*_{land_year}Ma.nc')
    land = xr.open_mfdataset(file)
    return land

def regrid_continent_maps(remap_file):

    land_year = f'{remap_file.strip(".nc").split("_")[-1]}'
    land = xr.open_mfdataset(remap_file)
    
    regrid_continent_data(land,land_year)
