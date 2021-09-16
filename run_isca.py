import ecrlisca.environment
from ecrlisca.misc.utils import land_year_range,min_land_year,max_land_year
import os
import argparse
from multiprocessing import cpu_count
import glob

parser=argparse.ArgumentParser(description="Run ISCA")
parser.add_argument('-multiplier',default=1,help="CO2 Multiplier")
parser.add_argument('-co2',default=None, help="CO2 Value")
parser.add_argument('-land_year',default=0,type=land_year_range,metavar=f'[{min_land_year}-{max_land_year}]',help="Years prior to current era in units of Ma")
parser.add_argument('-sea_level',default=0,type=float)
parser.add_argument('-ncores',default=32,type=int)
parser.add_argument('-nyears',default=20,type=int)
parser.add_argument('-overwrite',action='store_true')
args=parser.parse_args()

cmd = f'python experiments/variable_co2_and_continents.py'
cmd += f' -multiplier {args.multiplier}'
cmd += f' -land_year {args.land_year}'
cmd += f' -sea_level {args.sea_level}'
cmd += f' -nyears {args.nyears}'
cmd += f' -ncores {args.ncores}'
cmd += f' -co2 {args.co2}'
if args.overwrite:
    cmd += f' -overwrite'

os.system(cmd)
