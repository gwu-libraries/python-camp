#!/bin/bash

# Create test user in the container on startup
echo "Creating user jupytertest"
useradd -m -d /home/jupytertest -p $(openssl passwd password) jupytertest

# Launch the hub
exec jupyterhub