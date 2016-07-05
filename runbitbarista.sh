#!/bin/bash

clear

cd ~/BitBarista

electrum daemon start

xdg-open http://localhost:5000/ &

python ~/BitBarista/fserver.py
