#!/bin/bash

echo "Mounting storage"

bash ./scripts/storage.sh

echo "Downloading and installing isca"

python ./scripts/init_isca.py

echo "Installing packages"

python ./scripts/init_env.py
