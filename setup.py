from distutils.core import setup

setup(
    name='ecrlisca',
    version='0.1.0',
    url='https://github.com/bnb32/isca_aws',
    author='Brandon N. Benton',
    description='for running isca on aws',
    packages=['ecrlisca'],
    package_dir={'ecrlisca':'./ecrlisca'},
    install_requires=[
        'ecrlgcm',
        'matplotlib',
        'xarray',
        'cartopy',
        'netCDF4',
        'ffmpeg',
        'xesmf',
        'jupyterlab',
        'dash',
        'flask']
)
