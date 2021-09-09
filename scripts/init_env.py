import sys
sys.path.append('../')
sys.path.append('./')
import environment as env
import os

cmd='sudo yum-config-manager --enable epel; '
cmd+='sudo yum install openmpi-devel \
                       curl-devel \
                       environment-modules \
                       cmake \
                       ncl \
                       gftp \
                       blas-devel \
                       lapack-devel \
                       blas \
                       lapack \
                       "perl(XML::LibXML)"; '

if os.path.isfile('/usr/share/modules'): 
    cmd+='sudo mv /usr/share/modules /usr/share/Modules; '

os.system(cmd)

#build netcdf

PWD=env.BASE_DIR
CC='CC=/usr/lib64/openmpi/bin/mpicc'

cmd='export CC=/usr/lib64/openmpi/mpicc; '

# copy to bashrc
cmd+='export PATH=$PATH:/usr/lib64/openmpi/bin; '
cmd+='export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib; '
cmd+='export NETCDF_PATH=/usr/local/bin; '

#export PATH=$PATH:/usr/lib64/openmpi/bin
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
#export NETCDF_PATH=/usr/local/bin

os.system(cmd)
os.chdir(PWD)

if os.path.isfile('zlib-1.2.11.tar.gz'):
    os.system('rm zlib-1.2.11.tar.gz')

cmd='wget https://zlib.net/zlib-1.2.11.tar.gz; '
cmd+='tar xvf zlib-1.2.11.tar.gz; '
cmd+='cd zlib-1.2.11; '
cmd+='./configure --prefix=/usr/local/zlib; '
cmd+='make; ' 
cmd+='sudo make install; '
cmd+='cd ../; '
cmd+='rm -rf zlib-1.2.11*; '

os.system(cmd)
os.chdir(PWD)

if os.path.isfile('hdf5-1.10.5.tar.gz'):
    os.system('rm hdf5-1.10.5.tar.gz')
    
cmd='wget https://support.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.10.5.tar.gz; '
cmd+='tar xvf hdf5-1.10.5.tar.gz; '
cmd+='cd hdf5-1.10.5; '
#cmd+='./configure %s --with-zlib=/usr/local/zlib --prefix=/usr/local/ --enable-shared --enable-parallel; ' %(CC)
cmd+='./configure %s --with-zlib=/usr/local/zlib --prefix=/usr/local/; ' %(CC)
cmd+='make; '
cmd+='sudo make install; '
cmd+='cd ../; '
cmd+='rm -rf hdf5-1.10.5*; '

os.system(cmd)
os.chdir(PWD)

#if os.path.isfile('pnetcdf-1.12.2.tar.gz'):
#    os.system('rm pnetcdf-1.12.2.tar.gz')

#cmd='wget https://parallel-netcdf.github.io/Release/pnetcdf-1.12.2.tar.gz; '
#cmd+='tar xvf pnetcdf-1.12.2.tar.gz; '
#cmd+='cd pnetcdf-1.12.2; '
#cmd+='./configure; '
#cmd+='make; '
#cmd+='sudo make install; '
#cmd+='cd ../; '
#cmd+='rm -rf pnetcdf-1.12.2*; '

#os.system(cmd)
#os.chdir(PWD)

if os.path.isfile('netcdf-c-4.8.0.tar.gz'):
    os.system('rm netcdf-c-4.8.0.tar.gz')

cmd='wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-c-4.8.0.tar.gz; '
cmd+='tar xvf netcdf-c-4.8.0.tar.gz; '
cmd+='cd netcdf-c-4.8.0; '
#./configure --prefix=/usr/local CPPFLAGS=-I/usr/local/include LDFLAGS=-L/usr/local/lib --enable-parallel-tests --enable-pnetcdf 
#cmd+='./configure %s --prefix=/usr/local CPPFLAGS=-I/usr/local/include LDFLAGS=-L/usr/local/lib --enable-parallel-tests; ' %(CC)
cmd+='./configure %s --prefix=/usr/local CPPFLAGS=-I/usr/local/include LDFLAGS=-L/usr/local/lib; ' %(CC)
cmd+='make; '
cmd+='sudo make install; '
cmd+='cd ../; '
cmd+='rm -rf netcdf-c-4.8.0*; '

os.system(cmd)
os.chdir(PWD)

if os.path.isfile('netcdf-fortran-4.5.3.tar.gz'):
    os.system('rm netcdf-fortran-4.5.3.tar.gz')

cmd='wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-4.5.3.tar.gz; '
cmd+='tar xvf netcdf-fortran-4.5.3.tar.gz; '
cmd+='cd netcdf-fortran-4.5.3; '
cmd+='./configure %s; ' %(CC)
cmd+='make; '
cmd+='sudo make install; '
cmd+='cd ../; '
cmd+='rm -rf netcdf-fortran-4.5.3*; '

os.system(cmd)

