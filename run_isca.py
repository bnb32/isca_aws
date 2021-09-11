import environment as env
import os
import argparse

parser=argparse.ArgumentParser(description="Run ISCA")
parser.add_argument('-exp')
args=parser.parse_args()

if args.exp == 'co2':
    exp = 'test_cases/variable_co2_concentration/'
    script = 'variable_co2_grey.py'

elif args.exp == 'drycore':
    exp = 'test_cases/held_suarez/'
    script = 'held_suarez_test_case.py'

cmd = "cd %s/exp/%s" %(env.GFDL_BASE,exp)
cmd += "; python %s" %(script)

os.system(cmd)
