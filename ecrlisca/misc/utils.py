import ecrlisca.environment
import glob
import os

land_years = glob.glob(os.environ.get("RAW_TOPO_DIR")+'/Map*.nc')
land_years = sorted([float(l.strip('Ma.nc').split('_')[-1]) for l in land_years])
min_land_year = int(min(land_years))
max_land_year = int(max(land_years))

def land_year_range(arg):
    f = float(arg)
    if f < min_land_year or f > max_land_year:
        raise argparse.ArgumentTypeError(f'Argument must be < {max_land_year} and > {min_land_year}')
    return arg

def none_or_str(arg):
    if arg == 'None':
        return None
    return arg

