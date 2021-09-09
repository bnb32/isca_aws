#!/bin/bash

CONDA_DIR="/data/team/conda"

if [ ! -d "$CONDA_DIR" ];
then
    echo "Installing ECRL Conda environments to $CONDA_DIR"
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/conda.sh
    bash /tmp/conda.sh -b -p $CONDA_DIR
    rm -f /tmp/conda.sh
fi

# Add conda to PATH if it's not present
#grep -q -F "PATH=$CONDA_DIR/bin:\$PATH" ~/.bash_profile || \
#    echo "export PATH=$CONDA_DIR/bin:\$PATH" >> ~/.bash_profile
grep -q -F "source $CONDA_DIR/etc/profile.d/conda.sh" ~/.bashrc || \
    echo "source $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.bashrc
    
echo "WARNING: You may need to start a new terminal to use conda"
