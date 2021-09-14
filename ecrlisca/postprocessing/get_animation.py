import os
import glob
import argparse
from ecrlisca.postprocessing.utils import get_animation, define_land_colormap
import ecrlisca.environment
from ecrlisca.experiment import Experiment
import warnings
warnings.filterwarnings("ignore")

land_years = glob.glob(f'{os.environ.get("ISCA_REPO_DIR")}/experiments/input/land_masks/continents_*.nc')
land_years = sorted([l.strip('.nc').split('_')[-1] for l in land_years],key=lambda x:float(x.strip('Ma')))

parser = argparse.ArgumentParser(description="Get ISCA Animation")
parser.add_argument('-multiplier',default=2,help="CO2 Multiplier")
parser.add_argument('-land_year',default="0Ma",choices=land_years)
parser.add_argument('-field',default='t_surf')
parser.add_argument('-level',default=None)
args=parser.parse_args()

exp = Experiment(multiplier=args.multiplier,land_year=args.land_year)

define_land_colormap()
get_animation(exp,field=args.field,level=args.level)
