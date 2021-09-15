import json
import ecrlisca.environment
import os

def get_co2_series():
    f = open(os.path.join(os.environ.get('ISCA_REPO_DIR'),'ecrlisca/data/co2.txt'),'r')
    lines = f.readlines()
    lines = [l.strip('\n').split() for l in lines]
    lines = {-int(l[0]): float(l[1])*300.0 for l in lines}
    return lines
