#!/bin/bash

mkdir -p /data/deployment_data/julolo/log
mkdir -p /data/deployment_data/julolo/tmp

cd /var/www/julolo/ && git stash save --keep-index && git stash drop
cd /var/www/julolo/ && find . -name \*.pyc -delete
cd /var/www/julolo/ && git pull origin master

for arg in $@
do
  if [ $arg = "-r" -o $arg = "--refresh" ]
    then
      echo 'Refresh ...'
      cd /var/www/julolo/server/ &&
      python toolkits.py migration -p &&
      python toolkits.py index -p
  fi
done

sudo supervisorctl restart julolo
sudo supervisorctl restart julolo_master
