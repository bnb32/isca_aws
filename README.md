# isca_aws #

code for setting up and running isca on aws

1. Run `pip install -e .` to install module

2. Run `go.sh` to download required data and build environment

3. Run `run_isca.py -multiplier <multiplier> -land_year <land_year>` for simulations. Output in directory defined in `ecrlisca/environment.py`.

4. Modify namelist in `experiments/` to change simulation

5. Run `ecrlisca/posprocessing/get_animation.py -multiplier <multiplier> -land_year <land_year> -field <field> -level <level>` to create animation. Output in directory defined in `ecrlisca/environment.py`.
