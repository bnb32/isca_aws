import ecrlisca.environment
import os
import glob

class Experiment:
    def __init__(self,multiplier=2,land_year="0Ma"):
        self.multiplier = multiplier
        self.land_year = land_year
        self.path_format = f'variable_co2_{self.multiplier}x_continents_{self.land_year}_experiment'
        self.file_path = os.path.join(os.environ.get('GFDL_DATA'),self.path_format)
        self.files = sorted(glob.glob(os.path.join(self.file_path,'run*/atmos_monthly.nc')))
        self.land_file = os.path.join(os.environ.get('ISCA_REPO_DIR'),f'experiments/input/land_masks/continents_{self.land_year}.nc')         
