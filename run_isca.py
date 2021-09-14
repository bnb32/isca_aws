import ecrlisca.environment
import os
import argparse
from multiprocessing import cpu_count
import glob

land_years = glob.glob(f'{os.environ.get("ISCA_REPO_DIR")}/experiments/input/land_masks/continents_*.nc')
land_years = sorted([l.strip('.nc').split('_')[-1] for l in land_years],key=lambda x: float(x.strip('Ma')))
land_year_vals = [float(l.strip('Ma')) for l in land_years]

def land_year_range(arg):
    f = float(arg.strip('Ma'))
    if f < min(land_year_vals) or f > max(land_year_vals):
        raise argparse.ArgumentTypeError(f'Argument must be < {max(land_year_vals)}Ma and > {min(land_year_vals)}Ma')
    return arg

parser=argparse.ArgumentParser(description="Run ISCA")
parser.add_argument('-multiplier',default=2,help="CO2 Multiplier")
parser.add_argument('-co2',default=None,help="CO2 Value")
parser.add_argument('-land_year',default="0Ma",type=land_year_range,metavar=f'[{int(min(land_year_vals))}Ma-{int(max(land_year_vals))}Ma]',help="Years prior to current era")
parser.add_argument('-ncores',default=32,type=int)
parser.add_argument('-nyears',default=5,type=int)
args=parser.parse_args()

cmd = f'python experiments/variable_co2_and_continents.py'
cmd += f' -multiplier {args.multiplier}'
cmd += f' -co2 {args.co2}'
cmd += f' -land_year {args.land_year}'
cmd += f' -nyears {args.nyears}'
cmd += f' -ncores {args.ncores}'
cmd += f' -overwrite'
os.system(cmd)
