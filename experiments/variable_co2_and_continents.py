import os

import numpy as np

from multiprocessing import cpu_count

import f90nml

from isca import IscaCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

import argparse

parser=argparse.ArgumentParser(description="Run variable co2 experiment")
parser.add_argument('-multiplier',default=2)
parser.add_argument('-land_year',default=0)
parser.add_argument('-nyears',default=5,type=int)
parser.add_argument('-ncores',default=32,type=int)
args=parser.parse_args()

NCORES = int(args.ncores)
base_dir = os.path.dirname(os.path.realpath(__file__))
# a CodeBase can be a directory on the computer,
# useful for iterative development
cb = IscaCodeBase.from_directory(GFDL_BASE)

# or it can point to a specific git repo and commit id.
# This method should ensure future, independent, reproducibility of results.
# cb = DryCodeBase.from_repo(repo='https://github.com/isca/isca', commit='isca1.1')

# compilation depends on computer specific settings.  The $GFDL_ENV
# environment variable is used to determine which `$GFDL_BASE/src/extra/env` file
# is used to load the correct compilers.  The env file is always loaded from
# $GFDL_BASE and not the checked out git repo.

cb.compile()  # compile the source code to working directory $GFDL_WORK/codebase

adjust_co2_script = os.path.join(base_dir,'../preprocessing/adjust_co2.py')
os.system(f'python {adjust_co2_script} -multiplier {args.multiplier}')

adjust_land_script = os.path.join(base_dir,'../preprocessing/adjust_continents.py')
os.system(f'python {adjust_land_script} -land_year {args.land_year}')

# create an Experiment object to handle the configuration of model parameters
# and output diagnostics
exp = Experiment(f'variable_co2_{args.multiplier}x_continents_{args.land_year}_experiment', codebase=cb)

exp.inputfiles = [os.path.join(base_dir,f'input/co2_{args.multiplier}x.nc'),
                  os.path.join(base_dir,f'input/land_masks/continents_{args.land_year}.nc'),
                  #os.path.join(base_dir,'input/sst_clim_amip.nc'), 
                  os.path.join(base_dir,'input/siconc_clim_amip.nc')]

#Tell model how to write diagnostics
diag = DiagTable()
diag.add_file('atmos_monthly', 30, 'days', time_units='days')

#Tell model which diagnostics to write
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('dynamics', 'zsurf') #need at least ps, pk, bk and zsurf to do vertical interpolation onto plevels from sigma
diag.add_field('atmosphere', 'precipitation', time_avg=True)
diag.add_field('mixed_layer', 't_surf', time_avg=True)
diag.add_field('dynamics', 'sphum', time_avg=True)
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'temp', time_avg=True)
diag.add_field('dynamics', 'vor', time_avg=True)
diag.add_field('dynamics', 'div', time_avg=True)
diag.add_field('two_stream', 'co2', time_avg=True)
#diag.add_field('rrtm_radiation', 'co2', time_avg=True)

exp.diag_table = diag

#Empty the run directory ready to run
exp.clear_rundir()

namelist_name = os.path.join(base_dir, 'namelist_basefile.nml')
nml = f90nml.read(namelist_name)
exp.namelist = nml

'''
    
    'surface_flux_nml': {
        'use_virtual_temp': False,
        'do_simple': True,
        'old_dtaudv': True    
    },

    #Use a large mixed-layer depth, and the Albedo of the CTRL case in Jucker & Gerber, 2017
    'mixed_layer_nml': {
        'tconst' : 285.,
        'prescribe_initial_dist':True,
        'evaporation':True,  
        'depth': 2.5,                          #Depth of mixed layer used
        'albedo_value': 0.38,                  #Albedo value used      
    },

    'qe_moist_convection_nml': {
        'rhbm':0.7,
        'Tmin':160.,
        'Tmax':350.   
    },
    
    'damping_driver_nml': {
        'do_rayleigh': True,
        'trayfric': -0.25,              # neg. value: time in *days*
        'sponge_pbottom':  5000., #Bottom of the model's sponge down to 50hPa
        'do_conserve_energy': True,    
    },

    'spectral_dynamics_nml': {
        'damping_order': 4,             
        'water_correction_limit': 200.e2,
        'reference_sea_level_press':1.0e5,
        'num_levels':25,      #How many model pressure levels to use
        'valid_range_t':[100.,800.],
        'initial_sphum':[2.e-6],
        'vert_coord_option':'input',#Use the vertical levels from Frierson 2006
        'surf_res':0.5,
        'scale_heights' : 11.0,
        'exponent':7.0,
        'robert_coeff':0.03
    },
    'vert_coordinate_nml': {
        'bk': [0.000000, 0.0117665, 0.0196679, 0.0315244, 0.0485411, 0.0719344, 0.1027829, 0.1418581, 0.1894648, 0.2453219, 0.3085103, 0.3775033, 0.4502789, 0.5244989, 0.5977253, 0.6676441, 0.7322627, 0.7900587, 0.8400683, 0.8819111, 0.9157609, 0.9422770, 0.9625127, 0.9778177, 0.9897489, 1.0000000],
        'pk': [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
       }
'''

exp.update_namelist({
    'spectral_init_cond_nml':{
        'topog_file_name': f'continents_{args.land_year}.nc',
        'topography_option': 'input'
    },

    'two_stream_gray_rad_nml': {
        'rad_scheme':  'byrne',        
        'atm_abs': 0.2,                      # Add a bit of solar absorption of sw
        'do_seasonal':  True,          #do_seasonal=false uses the p2 insolation profile from Frierson 2006. do_seasonal=True uses the GFDL astronomy module to calculate seasonally-varying insolation.
        'equinox_day':  0.75,          #A calendar parameter to get autumn equinox in september, as in the standard earth calendar.
        'do_read_co2':  True, #Read in CO2 timeseries from input file
        'co2_file':  f'co2_{args.multiplier}x', #Tell model name of co2 input file        
    },


    'idealized_moist_phys_nml': {
        'do_damping': True,
        'turb':True,
        'mixed_layer_bc':True,
        'do_virtual' :False,
        'do_simple': True,
        'roughness_mom':3.21e-05,
        'roughness_heat':3.21e-05,
        'roughness_moist':3.21e-05,            
        'do_rrtm_radiation':False,
        'two_stream_gray': True,     #Use the grey radiation scheme
        'convection_scheme': 'SIMPLE_BETTS_MILLER', #Use simple Betts miller convection            
        'land_option': 'input',
        'land_file_name' : f'INPUT/continents_{args.land_year}.nc',
    }
})

'''
    
    'rrtm_radiation_nml': {
        'do_read_ozone':False,
        'solr_cnst': 1360., #s set solar constant to 1360, rather than default of 1368.22
        'dt_rad': 4320, #Use 4320 as RRTM radiation timestep
        'do_read_co2': True, #Read in CO2 timeseries from input file
        'co2_file':  f'co2_{args.multiplier}x', #Tell model name of co2 input file        
    },

    'idealized_moist_phys_nml': {
        'do_damping':True,
        'turb':True,
        'mixed_layer_bc':True,
        'do_virtual':False,
        'do_simple':True,
        'two_stream_gray':False,
        'do_rrtm_radiation':True,
        'convection_scheme': 'FULL_BETTS_MILLER',
        'land_option': 'input',
        'land_roughness_prefactor': 10.0,
        'roughness_mom': 2.e-04,
        'roughness_heat': 2.e-04,
        'roughness_moist': 2.e-04,
        'land_file_name' : f'INPUT/continents_{args.land_year}.nc',
    }
'''
#})

#Lets do a run!
if __name__=="__main__":
    exp.run(1, use_restart=False, num_cores=NCORES)
    for i in range(2,12*int(args.nyears)+1):
        exp.run(i, num_cores=NCORES)
