import os,sys
import ecrlisca.environment
import argparse

parser=argparse.ArgumentParser(description="Initialize ISCA")
args=parser.parse_args()

cmd=f'git clone https://github.com/ExeClim/Isca {os.environ["GFDL_BASE"]}'
cmd+=f'; cd os.environ["GFDL_BASE"]}'
cmd+='; conda env create -f ci/environment-py3.9.yml'
cmd+='; conda activate isca_env'

os.system(cmd)

cmd=f'cd {os.environ["GFDL_BASE"]}'
cmd+='; cd src/extra/python/'
cmd+='; pip install -e .'

os.system(cmd)
