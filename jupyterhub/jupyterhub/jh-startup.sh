#!/bin/bash

# Create test user in the container on startup
useradd -m -d /home/jupytertest -p password jupytertest

# Launch the hub
exec jupyterhub