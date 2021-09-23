# isca_aws #

code for setting up and running isca on aws

Install module:
```
pip install -e .
```

Download required data and build environment:
```
go.sh
```

Run simulations:
```
run_isca.py -multiplier <multiplier> -land_year <land_year>
```

Simulation output in directory defined in `ecrlisca/environment.py`.

Modify namelist in `experiments/` to change simulation

Create animations:
```
ecrlisca/posprocessing/get_animation.py -multiplier <multiplier> -land_year <land_year> -field <field> -level <level>
```
Animation output in directory defined in `ecrlisca/environment.py`.
