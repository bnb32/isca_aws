import os

years = [0,3,5,10,55,65,100,230,500]

for y in years:
    cmd = f'python run_isca.py -land_year {y}'
    os.system(cmd)
