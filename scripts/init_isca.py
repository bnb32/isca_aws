import os,sys
sys.path.append("../")
sys.path.append("./")
import environment as env
import argparse

parser=argparse.ArgumentParser(description="Initialize ISCA")
args=parser.parse_args()

cmd="git clone https://github.com/ExeClim/Isca %s" %(env.ISCA_DIR)
cmd+="; cd %s" %(env.ISCA_DIR)
cmd+="; conda env create -f ci/environment-py3.9.yml"
cmd+="; conda activate isca_env"

#os.system(cmd)

cmd="cd %s" %(env.ISCA_DIR)
cmd+="; cd src/extra/python/"
cmd+="; pip install -e ."

os.system(cmd)
