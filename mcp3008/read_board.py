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
serbatoio = 0   #pin 10
al_fondi = 1    #pin 12
al_generico = 2 #pin 14
al_calcif = 3   #pin 16
premacinato = 4 #pin 18
tazza1 = 5      #pin 21
tazza2 = 6      #pin 23
vapore = 7      #pin 25

serbatoio_readings = []
tazza1_readings = []
serbatoio_average  = 0
tazza1_average  = 0

while True:
        serbatoio_value = readadc(serbatoio, SPICLK, SPIMOSI, SPIMISO, SPICS) # read the analog pin
        serbatoio_value = serbatoio_value / 10.24 # convert 10bit adc0 (0-1024) trim pot read into 0-100 value
        serbatoio_readings.append(serbatoio_value)

        tazza1_value = readadc(tazza1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        tazza1_value = tazza1_value / 10.24
        tazza1_readings.append(tazza1_value)
        
        if len(serbatoio_readings) >= 100:
                serbatoio_average  = sum(serbatoio_readings)/len(serbatoio_readings)
                tazza1_average     = sum(tazza1_readings)/len(tazza1_readings)
                
                print time.time(),
                print ", ", serbatoio_average,
                print ", ", tazza1_average

                serbatoio_readings = []
                tazza1_readings    = []

        # hang out and do nothing for a half second
        time.sleep(0.0005)
