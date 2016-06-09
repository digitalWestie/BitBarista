#!/bin/bash

clear

electrum daemon start

python ~/BitBarista fserver.py

xdg-open http://localhost:5000/