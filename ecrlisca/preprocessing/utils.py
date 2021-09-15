import ecrlisca.environment
from ecrlisca.data.co2 import series as co2series
import os
import netCDF4 as nc
import numpy as np
import glob
import xarray as xr
import xesmf as xe
import warnings
warnings.filterwarnings("ignore")

def solar_constant(land_year):
    #assuming years prior to current era is expressed as a positive value
    time = -float(land_year.strip('Ma'))/4700.0
    return 1370.0/(1-0.4*time)

def interp(a,b,dt):
    return a*(1-dt)+dt*b

def interpolate_co2(land_year):

    year = float(land_year.strip('Ma'))

    keys = sorted(co2series,key=lambda x: float(x))
    kf = [float(k) for k in keys]

    if year in kf:
        return co2series[land_year.strip('Ma')]

    for i,k in enumerate(keys):
        if i==0:
            if year < kf[i]:
                return co2series[k]
        elif i==len(keys)-1:
            if year > kf[i]:
                return co2series[k]
        elif kf[i] < year < kf[i+1]:
            return interp(co2series[keys[i]],
                          co2series[keys[i+1]],
                          (year-kf[i])/(kf[i+1]-kf[i]))

def adjust_co2(multiplier=2,land_year='0Ma',co2_value=None,outfile=None):

    if outfile is None:
        if co2_value is None:
            outfile = f'co2_{multiplier}x_continents_{land_year}'
        else:
            outfile = f'co2_{co2_value}ppm_continents_{land_year}'

    base_dir = os.path.dirname(os.path.realpath(__file__))
    co2_path = os.environ.get('RAW_CO2_DIR')
    input_dir = os.environ.get('CO2_DIR')
    new_file = os.path.join(input_dir,f'{outfile}.nc')

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

land_years = glob.glob(os.environ.get("RAW_TOPO_DIR")+'/Map*.nc')
land_years = sorted([l.strip('Ma.nc').split('_')[-1] for l in land_years],key=lambda x: float(x.strip('Ma')))

def adjust_continents(land_year):
    land = interpolate_land(land_year)
    regrid_continent_data(land,land_year=land_year)

def regrid_continent_data(land,land_year="0Ma"):

    base = xr.open_mfdataset(os.environ.get('BASE_TOPO_FILE'))

    ds_out = xr.Dataset({'lat': (['lat'], base['lat'].values),
                         'lon': (['lon'], base['lon'].values)})

    out_file = f'continents_{land_year}.nc'

    out_dir = os.path.join(os.environ.get('TOPO_DIR'))
    out_file = os.path.join(out_dir,out_file)

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

def interpolate_land(land_year):
    year = float(land_year.strip('Ma'))

    keys = sorted(land_years,key=lambda x:float(x))
    kf = [float(k) for k in keys]

    if year in kf:
        return get_original_map_data(land_year)

    for i,k in enumerate(keys):
        if i==0:
            if year < kf[i]:
                return get_original_map_data(k)
        elif i==len(keys)-1:
            if year > kf[i]:
                return get_original_map_data(k)
        elif kf[i] < year < kf[i+1]:
            ds_out = get_original_map_data(keys[i])
            tmp = interp(get_original_map_data(keys[i])['z'].values,
                         get_original_map_data(keys[i+1])['z'].values,
                         (year-kf[i])/(kf[i+1]-kf[i]))
            ds_out['z'] = (ds_out['z'].dims,tmp)
            return ds_out

def get_original_map_data(land_year):
    land_year = str(land_year).strip('Ma')
    file = glob.glob(os.environ.get("RAW_TOPO_DIR")+'/Map*_{land_year}Ma.nc')
    land = xr.open_mfdataset(file)
    return land

def regrid_continent_maps(remap_file):

    land_year = f'{remap_file.strip(".nc").split("_")[-1]}'
    land = xr.open_mfdataset(remap_file)
    
    regrid_continent_data(land,land_year)
