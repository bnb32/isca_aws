import ecrlisca.environment
from ecrlisca.misc import sig_round
from ecrlisca.preprocessing import solar_constant
from ecrlisca.experiment import Experiment

import xarray as xr
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.animation as anim
from IPython.display import HTML
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import unregister_cmap
import os

def potential_intensity(t_surf):
    A = 28.2
    B = 55.8
    C = 0.1813
    T0 = 30.0+273.15
    return A+B*np.exp(C*(t_surf-T0))

def define_land_colormap():

    ncolors = 256
    color_array = plt.get_cmap('gray')(range(ncolors))[::-1]
    map_object = LinearSegmentedColormap.from_list(name='land_cmap',colors=color_array)

    # register this new colormap with matplotlib
    unregister_cmap('land_cmap')
    plt.register_cmap(cmap=map_object)

def get_data(experiment,field='t_surf',level=None,decode_times=True,anomaly=False):
    data = xr.open_mfdataset(experiment.files,decode_times=decode_times)
    land = xr.open_mfdataset(os.path.join(os.environ.get('TOPO_DIR'),experiment.land_file),
            decode_times=False)
    
    if field=='potential_intensity':
        pi = potential_intensity(data['t_surf'].values)
        data[field] = (data['t_surf'].dims,pi)
        data[field].attrs['long_name'] = 'potential intensity'
        data[field].attrs['units'] = 'm/s'

    if anomaly:
        #tmp = xr.open_mfdataset(Experiment(land_year=0).files,decode_times=decode_times) 
        tmp = get_data(Experiment(land_year=0),field=field,level=level,anomaly=False)
        data[field] = (tmp[field].dims,data[field].values-tmp[field].values.mean())
    
    if field=='potential_intensity':
        data[field] = (data[field].dims,np.multiply(data[field].values,np.array(land['land_mask'].values < 1.0, dtype=float)))        

    if 'co2' in data:
        tmp = data[[field,'co2']]
    else:
        tmp = data[[field]]
    
    tmp['land_mask'] = (land['land_mask'].dims,land['land_mask'].values)

    if 'pfull' in tmp[field].dims:
        if level is None:
            level = 250
        levels = np.array(tmp['pfull'].values)
        level = levels[np.argmin(np.abs(levels-level))]
        
        tmp[field] = tmp[field].sel(pfull = level)
    
    return tmp

def get_avg_field(exp,field='t_surf',level=None,vmin=None,vmax=None,anomaly=False):

    data = get_data(exp,field=field,level=level,decode_times=True,anomaly=anomaly)

    land = data['land_mask']
# Setup the initial plot
    if 'co2' in data:
        co2 = data['co2']

    variable = data[field]

    lons = sorted(variable.lon.values)

    fig = plt.figure(figsize=(10,5))
    proj = ccrs.PlateCarree(central_longitude=180.0)
    ax = plt.axes(projection=proj)

    if 'time' in variable.dims:
        avg = variable.mean(dim='time')
    else:
        avg = variable

    image = avg.plot.imshow(ax=ax, transform=proj,
                            interpolation='bilinear',cmap="coolwarm",
                            animated=True, add_colorbar=False,
                            )

    if land is not None:
        land_img = land.plot.contour(ax=ax, transform=ccrs.PlateCarree(),
                                     cmap="land_cmap",
                                     add_colorbar=False,
                                     alpha=1.0,
                                    )
    else:
        ax.coastlines()

    try:
        cb = plt.colorbar(image, ax=ax, orientation='horizontal', pad=0.05, label=f'{variable.long_name} ({variable.units})')
    except:
        cb = plt.colorbar(image, ax=ax, orientation='horizontal', pad=0.05, label=f'{variable.name}')

    if vmin is None or vmax is None:
        image.set_clim(variable.values.min(),variable.values.max())
    else:
        image.set_clim(vmin,vmax)

    text = cb.ax.xaxis.label
    font = matplotlib.font_manager.FontProperties(size=16)
    text.set_font_properties(font)

    image.set_array(avg.sel(lon=lons))

    if 'co2' in data:
        ax.set_title(f'Time Average, CO2 = {sig_round(co2.values.mean(),4)} ({co2.units}), solar constant = {sig_round(solar_constant(exp.land_year),4)} (W/m**3)',fontsize=20)
    else:
        ax.set_title(f'Time Average',fontsize=20)

def get_animation(exp,field='t_surf',level=None,vmin=None,vmax=None,anomaly=False):

    data = get_data(exp,field=field,level=level,decode_times=True,anomaly=anomaly)
    land = data['land_mask']
    
# Setup the initial plot
    if 'co2' in data:
        co2 = data['co2']

    variable = data[field]

    fig = plt.figure(figsize=(12,7))
    proj = ccrs.PlateCarree(central_longitude=180.0)
    ax = plt.axes(projection=proj)

    image = variable.mean(dim='time').plot.imshow(ax=ax, transform=proj, 
                                                  interpolation='bilinear',cmap="coolwarm", 
                                                  animated=True, add_colorbar=False)
    
    
    if land is not None:
        land_img = land.plot.contour(ax=ax, transform=ccrs.PlateCarree(), 
                                     cmap="land_cmap", 
                                     add_colorbar=False,
                                     alpha=1.0,
                                    )
    else:
        ax.coastlines()
    
    
    try:
        cb = plt.colorbar(image, ax=ax, orientation='horizontal', pad=0.05, label=f'{variable.long_name} ({variable.units})')
    except:
        cb = plt.colorbar(image, ax=ax, orientation='horizontal', pad=0.05, label=f'{variable.name}')
    
    if vmin is None or vmax is None:
        avg = variable.mean(dim=['time'])
        std = np.std(variable.values)
        
        vmin = variable.values.min()#avg.values.min()-2*std
        vmax = variable.values.max()#avg.values.max()+2*std

        print(f"plotting with vmin={vmin}, vmax={vmax}")
        image.set_clim(vmin,vmax)
    else:
        image.set_clim(vmin,vmax)
        
    text = cb.ax.xaxis.label
    font = matplotlib.font_manager.FontProperties(size=16)
    text.set_font_properties(font)
    
    def update(i):
        t = variable.time.values[i]
        if 'co2' in data:
            ax.set_title(f'time = {t.strftime("%B %Y")}, co2 = {sig_round(co2[i].values.mean(),4)} ({co2.units}), solar constant = {sig_round(solar_constant(exp.land_year),4)} (W/m**3)',fontsize=20)
        else:
            ax.set_title(f'time = {t.strftime("%B %Y")}',fontsize=20)
            
        image.set_array(variable.sel(time=t))
        return image
    
    plt.close()
    animation = anim.FuncAnimation(fig, update, frames=range(len(variable.time)), blit=False)
    writervideo = anim.FFMpegWriter(fps=5) 
    anim_file = os.path.join(os.environ.get('ISCA_REPO_DIR'),f'ecrlisca/postprocessing/anims/{exp.path_format}_{field}')
    if anomaly:
        anim_file += '_anomaly.mp4'
    else:
        anim_file += '.mp4'
    animation.save(anim_file, writer=writervideo)
    print(anim_file)
    #return HTML(animation.to_jshtml())        
