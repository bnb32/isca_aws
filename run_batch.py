import os

years = [0,0.02,3,5,10,55,65,100,230,500]

for y in years:
    cmd = f'python run_isca.py -land_year {y} -overwrite'
    if y==0.02: cmd+=' -sea_level -100'
    os.system(cmd)
