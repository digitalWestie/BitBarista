#!/bin/bash

clear

cd ~/BitBarista

sleep 2s;

sudo -u pi epiphany-browser -a --profile ~/.config http://localhost:5000 --display=:0 &


