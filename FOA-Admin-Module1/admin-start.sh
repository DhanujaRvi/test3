#!/bin/bash
echo "Admin Start Script Running"
cd /home/ubuntu/Payables-Admin-Module
cd configs
sudo docker-compose up -d
source environ.sh
cd ..
nohup python flaskApp.py &
