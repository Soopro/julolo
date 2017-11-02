#!/bin/bash

for arg in $@
do
  if [ $arg = "-p" -o $arg = "--packages" ]
    then
      echo 'Setup Peon with reuiqred packages'
      sudo pip install -r requirements.txt
  fi
done

sudo python setup.py install
