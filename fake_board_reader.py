#!/usr/bin/env python
import time

def read_state():
  state = {"overall":"","serbatoio":"", "al_fondi":"", 
    "al_generico":"", "al_calcif":"", "premacinato":"", 
    "tazza1":"","tazza2":"","vapore":""}

  state["overall"] = 'ready'
  return state
