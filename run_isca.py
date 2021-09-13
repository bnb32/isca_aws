import environment as env
import os
import argparse
from multiprocessing import cpu_count

parser=argparse.ArgumentParser(description="Run ISCA")
parser.add_argument('-multiplier',default=2)
parser.add_argument('-land_year',default=0)
parser.add_argument('-ncores',default=32,type=int)
parser.add_argument('-nyears',default=5,type=int)
args=parser.parse_args()

cmd = f'python experiments/variable_co2_and_continents.py'
cmd += f' -multiplier {args.multiplier}'
cmd += f' -land_year {args.land_year}'
cmd += f' -nyears {args.nyears}'
cmd += f' -ncores {args.ncores}'
os.system(cmd)
