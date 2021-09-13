import os

cmd='sudo yum-config-manager --enable epel; '
cmd+='sudo yum install '
cmd+='netcdf \ 
      netcdf-fortran \
      ;'

os.system(cmd)

cmd='conda install -n isca_env -c conda-forge '
cmd+='xarray \
      xesmf \ 
      netCDF4 \
      ;'

os.system(cmd)
