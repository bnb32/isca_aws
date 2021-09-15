import ecrlisca.environment
import os
import argparse
from multiprocessing import cpu_count
import glob

land_years = glob.glob(f'{os.environ.get("TOPO_DIR")}/Map*.nc')
land_years = sorted([l.strip('.nc').split('_')[-1] for l in land_years],key=lambda x: float(x.strip('Ma')))
land_year_vals = [float(l.strip('Ma')) for l in land_years]
min_val = int(min(land_year_vals))
max_val = int(max(land_year_vals))

def land_year_range(arg):
    f = float(arg.strip('Ma'))
    if f < min_val or f > max_val:
        raise argparse.ArgumentTypeError(f'Argument must be < {max_val}Ma and > {min_val}Ma')
    return arg

parser=argparse.ArgumentParser(description="Run ISCA")
parser.add_argument('-multiplier',default=1,help="CO2 Multiplier")
parser.add_argument('-co2',default=None, help="CO2 Value")
parser.add_argument('-land_year',default="0Ma",type=land_year_range,metavar=f'[{min_val}Ma-{max_val}Ma]',help="Years prior to current era")
parser.add_argument('-ncores',default=32,type=int)
parser.add_argument('-nyears',default=5,type=int)
args=parser.parse_args()

cmd = f'python experiments/variable_co2_and_continents.py'
cmd += f' -multiplier {args.multiplier}'
cmd += f' -land_year {args.land_year}'
cmd += f' -nyears {args.nyears}'
cmd += f' -ncores {args.ncores}'
cmd += f' -overwrite'
cmd += f' -co2 {args.co2}'
os.system(cmd)
