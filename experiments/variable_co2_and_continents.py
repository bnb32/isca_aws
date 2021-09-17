import os

import numpy as np

from multiprocessing import cpu_count

import f90nml

from isca import IscaCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

import argparse

from ecrlisca.preprocessing.utils import adjust_co2, adjust_continents, solar_constant
from ecrlisca.experiment import Experiment as ecrlExp
from ecrlisca.misc.utils import none_or_str, land_year_range, min_land_year, max_land_year

parser=argparse.ArgumentParser(description="Run variable co2 experiment")
parser.add_argument('-multiplier',default=1)
parser.add_argument('-co2',default=None,type=none_or_str)
parser.add_argument('-land_year',default=0,type=land_year_range,metavar=f'[{min_land_year}-{max_land_year}]',help="Years prior to current era in units of Ma")
parser.add_argument('-sea_level',default=0,type=float)
parser.add_argument('-nyears',default=5,type=int)
parser.add_argument('-ncores',default=32,type=int)
parser.add_argument('-overwrite',action='store_true')
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
# create an Experiment object to handle the configuration of model parameters
# and output diagnostics
ecrlexp = ecrlExp(multiplier=args.multiplier,land_year=args.land_year,co2_value=args.co2)

exp = Experiment(ecrlexp.name, codebase=cb)

co2_file = ecrlexp.co2_file.split('.nc')[0]
land_file = ecrlexp.land_file

adjust_co2(multiplier=args.multiplier,land_year=args.land_year,co2_value=args.co2,outfile=co2_file)
adjust_continents(land_year=args.land_year,sea_level=args.sea_level)

exp.inputfiles = [os.path.join(base_dir,f'input/{co2_file}.nc'),
                  os.path.join(base_dir,f'input/land_masks/{land_file}'),
                  #os.path.join(base_dir,'input/sst_clim_amip.nc'), 
                  os.path.join(os.environ.get('GFDL_BASE'),'exp/test_cases/realistic_continents/input/siconc_clim_amip.nc')]

#Tell model how to write diagnostics
diag = DiagTable()
diag.add_file('atmos_monthly', 30, 'days', time_units='days')

#Tell model which diagnostics to write
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('atmosphere', 'bucket_depth', time_avg=True)
diag.add_field('dynamics', 'zsurf') #need at least ps, pk, bk and zsurf to do vertical interpolation onto plevels from sigma
diag.add_field('atmosphere', 'precipitation', time_avg=True)
diag.add_field('atmosphere', 'cape', time_avg=True)
diag.add_field('atmosphere', 'convection_rain', time_avg=True)
diag.add_field('atmosphere', 'condensation_rain', time_avg=True)
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

namelist_name = os.path.join(base_dir, 'variable_co2_and_continents.nml')
nml = f90nml.read(namelist_name)
exp.namelist = nml

exp.update_namelist({
    'spectral_init_cond_nml':{
        'topog_file_name': f'{land_file}',
        'topography_option': 'input'
    },

    #'rrtm_radiation_nml': { 
    #    #'do_read_ozone':True, 
    #    #'ozone_file':'ozone_1990', 
    #    'solr_cnst': solar_constant(args.land_year), #s set solar const    ant to 1360, rather than default of 1368.22 
    #    'dt_rad': 4320, #Use 4320 as RRTM radi    ation timestep 
    #    'do_read_co2': True, #Read in CO2 time    series from input file 
    #    'co2_file': f'{co2_file}' #Tell model name of     co2 input file         
    #},

    'two_stream_gray_rad_nml': {
        'rad_scheme':  'byrne',        
        'atm_abs': 0.2, # Add a bit of solar absorption of sw
        'do_seasonal':  True, #do_seasonal=True uses the GFDL astronomy module to calculate seasonally-varying insolation.
        'equinox_day':  0.75, #A calendar parameter to get autumn equinox in september, as in the standard earth calendar.
        'do_read_co2':  True, #Read in CO2 timeseries from input file
        'co2_file':  f'{co2_file}', #Tell model name of co2 input file        
        'solar_constant': solar_constant(args.land_year),
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
        #'do_rrtm_radiation':True,
        'two_stream_gray': True,     #Use the grey radiation scheme
        'convection_scheme': 'SIMPLE_BETTS_MILLER', #Use simple Betts miller convection            
        'land_option': 'input',
        'land_file_name' : f'INPUT/{land_file}',
    },    

})

#Lets do a run!
if __name__=="__main__":
    exp.run(1, use_restart=False, num_cores=NCORES, overwrite_data=args.overwrite)
    for i in range(2,12*int(args.nyears)+1):
        exp.run(i, num_cores=NCORES, overwrite_data=args.overwrite)
