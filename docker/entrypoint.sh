#!/bin/bash

# copy ssh keys so can set correct ownership
cp -r .ssh-keys/dbwebb .ssh-keys/dbwebb.pub .ssh/
chown -R $(id -u):$(id -g) .ssh
chmod 600 .ssh/*



# copy dbwebb config file so we can change path to ssh key
cp .dbwebb.config.real .dbwebb.config
sed -i 's/DBW_SSH_KEY=.*/DBW_SSH_KEY="\/home\/dbwebb\/.ssh\/dbwebb"/g' .dbwebb.config



# run gazi
cd /home/dbwebb/courses
exec "$@"
