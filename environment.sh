#!/bin/bash

USERNAME="ec2-user"
NETID="bnb32"
PROJECT_CODE="UCOR0044"
ROOT_DIR="/data/${NETID}"
SCRATCH_DIR="${ROOT_DIR}/scratch"
BASE_DIR="/home/${USERNMAME}/environment"
ISCA_DIR="${ROOT_DIR}/my_isca"
MAIN_DIR="${BASE_DIR}/isca_aws"

export GFDL_BASE=${ISCA_DIR}
export GFDL_ENV="aws"
export GFDL_WORK="${ROOT_DIR}/gfdl_work"
export GFDL_DATA="${ROOT_DIR}/gfdl_data"
