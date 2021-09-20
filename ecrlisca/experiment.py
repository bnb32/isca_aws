import ecrlisca.environment
import os
import glob

class Experiment:
    def __init__(self,multiplier=1,land_year=0,co2_value=None):
        self.multiplier = multiplier
        self.land_year = land_year
        self.path_format = f'variable_co2_{self.multiplier}x_continents_{self.land_year}Ma_experiment'
        self.file_path = os.path.join(os.environ['GFDL_DATA'],self.path_format)
        self.files = sorted(glob.glob(os.path.join(self.file_path,'run*/atmos_monthly.nc')))

        self.name = f'variable_co2_{multiplier}x_continents_{land_year}Ma_experiment'

        if co2_value is not None:
            self.co2_file = f'co2_{co2_value}ppm_continents_{land_year}Ma.nc'
        else:
            self.co2_file = f'co2_{multiplier}x_continents_{land_year}Ma.nc'
        
        self.land_file = f'continents_{land_year}Ma.nc'

        #self.solar_constant = solar_constant(land_year)

        #self.co2_value = interpolate_co2(land_year)
