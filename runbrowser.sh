#!/bin/bash

clear

cd ~/BitBarista

sleep 8s;

sudo -u pi epiphany-browser -a --profile ~/.config http://localhost:5000 --display=:0 &

sleep 3s;

xte "key F11" -x:0
