#!/usr/bin/env python
import time
from random import randint

def read_state():
  state = {"overall":"", "message":"", "serbatoio":"", "al_fondi":"", 
    "al_generico":"", "al_calcif":"", "premacinato":"", 
    "tazza1":"","tazza2":"","vapore":""}
  
  if randint(0,9) > 4:
    state["overall"] = 'ready'
  else:
    state["overall"] = ''
    state["message"] = "Water is missing, could you replace it?"

  return state

def cleanup():
  print "Cleaning up GPIO"