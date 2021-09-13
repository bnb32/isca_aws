import ecrlisca.environment
import os
import argparse
from multiprocessing import cpu_count
import glob

land_years = glob.glob(f'{os.environ.get("ISCA_REPO_DIR")}/experiments/input/land_masks/continents_*.nc')
land_years = sorted([l.strip('.nc').split('_')[-1] for l in land_years],key=lambda x: float(x.strip('Ma')))

parser=argparse.ArgumentParser(description="Run ISCA")
parser.add_argument('-multiplier',default=2,help="CO2 Multiplier")
parser.add_argument('-land_year',default="0Ma",choices=land_years,help="Years prior to current era")
parser.add_argument('-ncores',default=32,type=int)
parser.add_argument('-nyears',default=5,type=int)
args=parser.parse_args()

cmd = f'python experiments/variable_co2_and_continents.py'
cmd += f' -multiplier {args.multiplier}'
cmd += f' -land_year {args.land_year}'
cmd += f' -nyears {args.nyears}'
cmd += f' -ncores {args.ncores}'
os.system(cmd)
