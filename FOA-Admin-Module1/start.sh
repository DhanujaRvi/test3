#!/bin/bash
conda activate admin
cd Payables-Admin-Module
source configs/environ.sh 
nohup python flaskApp.py & $echo -ne '\n'

conda deactivate
cd .. 
cd Payables-Processor-Module
conda activate processor
cd configs
sudo docker-compose up -d
cd ..
cd DocIdentifier
sudo docker-compose up -d
cd ..
source configs/environ.sh 
nohup python flaskApp.py &

sudo netstat -nlp |grep python