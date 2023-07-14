#!/bin/bash

# Create test user(s) in the container on startup
for user in ${TEST_USERS//,/ }
do
    echo "Creating user ${user}"
    useradd -m -d /home/${user} -p $(openssl passwd password) ${user}
done
# Launch the hub
exec jupyterhub