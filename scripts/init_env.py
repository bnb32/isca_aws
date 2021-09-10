import sys
sys.path.append('../')
sys.path.append('./')
import environment as env
import os

cmd='sudo yum-config-manager --enable epel; '
cmd+='sudo yum install netcdf \
                       netcdf-fortran \
                       ; '

os.system(cmd)
