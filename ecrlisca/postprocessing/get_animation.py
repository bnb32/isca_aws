import os
import glob
import argparse
from ecrlisca.postprocessing.utils import get_animation, define_land_colormap
from ecrlisca.misc.utils import none_or_str, land_year_range, min_land_year, max_land_year
import ecrlisca.environment
from ecrlisca.experiment import Experiment
import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description="Get ISCA Animation")
parser.add_argument('-multiplier',default=1,help="CO2 Multiplier")
parser.add_argument('-land_year',default=0,type=land_year_range,metavar=f'[{min_land_year}-{max_land_year}]',help="Years prior to current era in units of Ma")
parser.add_argument('-field',default='t_surf')
parser.add_argument('-anomaly',action='store_true')
parser.add_argument('-vmin',type=none_or_str,default=None)
parser.add_argument('-vmax',type=none_or_str,default=None)
parser.add_argument('-level',default=None)
args=parser.parse_args()

exp = Experiment(multiplier=args.multiplier,land_year=args.land_year)

define_land_colormap()
get_animation(exp,
              field=args.field,
              level=args.level,
              anomaly=args.anomaly,
              vmin=args.vmin,
              vmax=args.vmax)
