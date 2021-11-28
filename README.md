# isca_aws #

Code for setting up and running isca on aws. Requires gcm_aws repo.

Install module:
```bash
pip install -e .
```

Modify environment variables:
```bash
vim ecrlisca/environment.py
```

Download required data and build environment:
```bash
bash go.sh
```

Run simulations:
```bash
python run_isca.py -multiplier <multiplier> -land_year <land_year>
```
Simulation output in directory defined in `ecrlisca/environment.py`.


Modify namelist in `experiments/` to change simulations.


Create animations:
```bash
python ecrlisca/posprocessing/get_animation.py -multiplier <multiplier> -land_year <land_year> -field <field> -level <level>
```
Animation output in directory defined in `ecrlisca/environment.py`.
