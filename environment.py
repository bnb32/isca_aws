import os

USERNAME="ec2-user"
NETID="bnb32"
PROJECT_CODE="UCOR0044"
ROOT_DIR="/data/%s" %(NETID)
SCRATCH_DIR=ROOT_DIR+"/scratch"
BASE_DIR="/home/%s/environment" %(USERNAME)
ISCA_DIR=ROOT_DIR+"/isca"
MAIN_DIR=BASE_DIR+"/isca_aws"
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
