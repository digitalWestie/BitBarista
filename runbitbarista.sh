#!/bin/bash

clear

cd ~/BitBarista

electrum daemon start

lxterminal -e python ~/BitBarista/fserver.py

