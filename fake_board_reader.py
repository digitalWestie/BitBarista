#!/usr/bin/env python
import time
from random import randint

def read_state():
  state = {"overall":"","serbatoio":"", "al_fondi":"", 
    "al_generico":"", "al_calcif":"", "premacinato":"", 
    "tazza1":"","tazza2":"","vapore":""}
  
  if randint(0,9) > 2:
    state["overall"] = 'ready'
  else:
    state["overall"] = ''

  return state
