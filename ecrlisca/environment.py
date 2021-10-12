import os

USERNAME="ec2-user"
NETID="bnb32"
PROJECT_CODE="UCOR0044"
ROOT_DIR="/data/%s" %(NETID)
SCRATCH_DIR=ROOT_DIR+"/scratch"
BASE_DIR="/home/%s/environment" %(USERNAME)
ISCA_DIR=ROOT_DIR+"/isca"

ISCA_REPO_DIR=BASE_DIR+"/isca_aws"
os.environ['ISCA_REPO_DIR'] = ISCA_REPO_DIR
# directory of the Isca source code
GFDL_BASE=ISCA_DIR
os.environ['GFDL_BASE'] = GFDL_BASE
# "environment" configuration for emps-gv4
#GFDL_ENV="gfortran"
GFDL_ENV="aws"
os.environ['GFDL_ENV'] = GFDL_ENV
# temporary working directory used in running the model
GFDL_WORK=ROOT_DIR+"/gfdl_work"
os.environ['GFDL_WORK'] = GFDL_WORK
# directory for storing model output
GFDL_DATA=ROOT_DIR+"/gfdl_data"
os.environ['GFDL_DATA'] = GFDL_DATA

RAW_TOPO_DIR =f'/data/{NETID}/paleodem_raw'
os.environ['RAW_TOPO_DIR'] = RAW_TOPO_DIR

TOPO_DIR = os.path.join(ISCA_REPO_DIR,'experiments/input/land_masks/')
os.environ['TOPO_DIR'] = TOPO_DIR

RAW_CO2_DIR = os.path.join(GFDL_BASE,'exp/test_cases/variable_co2_concentration/input/')
os.environ['RAW_CO2_DIR'] = RAW_CO2_DIR

CO2_DIR = os.path.join(ISCA_REPO_DIR,'experiments/input')
os.environ['CO2_DIR'] = CO2_DIR

os.environ['BASE_TOPO_FILE'] = os.path.join(GFDL_BASE,'input/land_masks/era_land_t42.nc')
