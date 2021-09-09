import environment as env
import os

cmd = "cd %s/exp/test_cases/held_suarez" %(env.GFDL_BASE)
cmd += "; python held_suarez_test_case.py"

os.system(cmd)

