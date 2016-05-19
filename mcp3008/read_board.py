#!/usr/bin/env python

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 0

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
  if ((adcnum > 7) or (adcnum < 0)):
          return -1
  GPIO.output(cspin, True)

  GPIO.output(clockpin, False)  # start clock low
  GPIO.output(cspin, False)     # bring CS low

  commandout = adcnum
  commandout |= 0x18  # start bit + single-ended bit
  commandout <<= 3    # we only need to send 5 bits here
  for i in range(5):
          if (commandout & 0x80):
                  GPIO.output(mosipin, True)
          else:
                  GPIO.output(mosipin, False)
          commandout <<= 1
          GPIO.output(clockpin, True)
          GPIO.output(clockpin, False)

  adcout = 0
  # read in one empty bit, one null bit and 10 ADC bits
  for i in range(12):
          GPIO.output(clockpin, True)
          GPIO.output(clockpin, False)
          adcout <<= 1
          if (GPIO.input(misopin)):
                  adcout |= 0x1

  GPIO.output(cspin, True)
  
  adcout >>= 1       # first bit is 'null' so drop it
  return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#MCP Channel to Control Mappings
# serbatoio   #pin 10
# al_fondi    #pin 12
# al_generico #pin 14
# al_calcif   #pin 16
# premacinato #pin 18
# tazza1      #pin 21
# tazza2      #pin 23
# vapore      #pin 25

channel_names = ["serbatoio","al_fondi","al_generico","al_calcif","premacinato","tazza1","tazza2","vapore"]
channel_readings   = [[],[],[],[],[],[],[],[]]
channel_averages   = []

while True:

  channel = 0
  while channel <= 7:
    channel_value = readadc(channel, SPICLK, SPIMOSI, SPIMISO, SPICS) # read the analog pin
    channel_value = round(channel_value / 10.24, 2) # convert 10bit adc0 (0-1024) trim pot read into 0-100 value
    channel_readings[channel].append(channel_value)
    channel+=1

  if len(channel_readings[0]) >= 150:
    print time.time(),
    channel = 0
    while channel <= 7:
      channel_average = sum(channel_readings[channel])/len(channel_readings[channel])
      print ",",channel_names[channel], 
      print ",",channel_average,
      if (channel==7):
        print ""
      channel+=1  

  # hang out and do nothing for a half second
  time.sleep(0.0005)
