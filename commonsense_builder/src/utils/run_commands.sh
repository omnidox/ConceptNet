#!/bin/bash

source concept_env/bin/activate
sudo systemctl stop postgresql
sudo docker start conceptnet5
sudo docker exec -it -w /conceptnet5/web conceptnet5 python3 conceptnet_web/api.py
