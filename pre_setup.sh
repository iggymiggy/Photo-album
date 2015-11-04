#!/bin/bash

#Script: pre_setup.sh
#This script is for setting up the virtualenvironment used in our project. Run in Ubuntu 13.10.

echo
echo "Updating Ubuntu"

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python-pip
sudo pip install virtualenvwrapper

cd
mkdir .virtualenvs
echo "export WORKON_HOME=$HOME/.virtualenvs" >> .profile
echo "export PROJECT_HOME=$HOME/dev" >> .profile
echo "export VIRTUALENV_PYTHON=/usr/bin/python3" >> .profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> .profile
