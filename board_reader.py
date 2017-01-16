#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #set up GPIO using BCM numbering
DEBUG = 0

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

# set up the optopins
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

CHANNEL_NAMES = ["serbatoio","al_fondi","al_generico","al_calcif","premacinato","tazza1","tazza2","vapore"]

#STEADY SIGNATURES:
READY_SIG = [0.0, 31.0, 2.1, 0.0, 0.0, 31.0, 31.0, 2.0]
TAZZA2_SIG = [0.055, 30.35, 0.0, 0.0, 0.01, 0.0, 30.7, 0.0]
WATER_EMPTY_SIG  = [0.0, 29.0, 0.0, 0.0, 0.0, 56.2, 29.5, 0.0]
EMPTY_GRINDS_SIG = [0.0, 57.49, 0.0, 0.0, 0.0, 30.4, 57.39, 0.0]
WATER_TRAY_SIG   = [0.0, 56.74, 0.0, 0.0, 0.0, 56.80, 56.67, 0.0] #both water empty and empty tray lights

#OFF SIGNATURES:
OFF_SIG = [0.0, 2.0, 2.0, 0.0, 0.10, 2.0, 2.0, 2.0]
OFF_AT_WALL_SIG = [0.0, 11.0, 11.0, 5.0, 2.10, 11.0, 10.5, 11.0]

#FLASHING SIGNATURES:
WARMUP_SIG          = [3.3, 16.98, 1.95, 0.5, 0.08, 16.59, 16.48, 1.6]
WARMUP_NO_WATER_SIG = [0.0, 14.68, 0.0,  0.0, 0.0,  41.2,  14.3,  0.0]
NO_BEANS_SINGLE_SIG = [0.12, 13.8, 0.0,  0.1, 0.01, 30.51, 13.85, 0.0]
NO_BEANS_DOUBLE_SIG = [0.08, 44.3, 0.0, 0.0026, 0.0, 0.0,  44.0,  0.0]
NO_BEANS_ALL_SIG    = [0.08, 44.0, 0.0, 0.0026, 0.0, 30.1, 43.7, 0.0] #shows after an empty dbl/single



# LED pin numbering from control board ribbon (NOT GPIO!)
# serbatoio   #pin 10
# al_fondi    #pin 12
# al_generico #pin 14
# al_calcif   #pin 16
# premacinato #pin 18
# tazza1      #pin 21
# tazza2      #pin 23
# vapore      #pin 25

# Button pin numbering from control board ribbon (NOT GPIO!)
# on/off: 3 & 5
# tazza1: 7 & 9
# tazza2: 11 & 13
# vapore: 15 & 17
# decalcif: 20 & 22
# premacinato: 24 & 26

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


def read_state():
  state = {"overall":"","serbatoio":"", "al_fondi":"", 
    "al_generico":"", "al_calcif":"", "premacinato":"", 
    "tazza1":"","tazza2":"","vapore":""}

  # 100 readings x 0.0005 pause = 0.05 
  # flash cycle = 6 * 0.05
  # on for 0.15, off for 0.15
  results = []

  results.append(collect_readings())
  results.append(collect_readings())
  results.append(collect_readings())
  results.append(collect_readings())
  results.append(collect_readings())
  results.append(collect_readings())

  all_channel_averages = []
  column_averages = [0,0,0,0,0,0,0,0]

  sample = 0
  while sample < len(results):
    avg = sum(results[sample])/len(results[sample])
    all_channel_averages.append(avg)
    for col in range(8):
      column_averages[col] += results[sample][col]
    sample+=1

  for col in range(8):
    column_averages[col] = column_averages[col]/len(results)
  
  #test if machine is off
  all_off=False
  all_off=test_sig(OFF_AT_WALL_SIG, column_averages)
  if not all_off:
    all_off = test_sig(OFF_SIG, column_averages)
        
  if all_off:
    state["overall"] = 'off'
    state["message"] = "Machine is off, or warming up."
  elif test_sig(WATER_EMPTY_SIG, column_averages) or test_sig(WATER_TRAY_SIG, column_averages):
    state["overall"] = 'water'
    state["message"] = "Water is missing, could you replace it?"
  elif test_sig(READY_SIG, column_averages):
    state["overall"] = 'ready'
    state["message"] = "Ready to serve!"
  elif test_sig(EMPTY_GRINDS_SIG, column_averages):
    state["overall"] = 'empty_grinds'
    state["message"] = "The coffee grinds tray is full, can you empty it?"
  elif test_steady(all_channel_averages):
    state["overall"] = 'steady'
    state["message"] = "Something's not right!"
    print "Channels are steady"
    print "Channel averages: ", all_channel_averages
    print "Column averages: ", column_averages
  else:
    if test_sig(NO_BEANS_DOUBLE_SIG, column_averages):
      state["overall"] = 'no_beans'
      state["message"] = "There are no more beans left!"
    elif test_sig(NO_BEANS_SINGLE_SIG, column_averages):
      state["overall"] = 'no_beans'
      state["message"] = "There are no more beans left!"
    elif test_sig(WARMUP_SIG, column_averages):
      state["overall"] = 'warmup'
      state["message"] = "Warming up and flushing pipes."
    elif test_sig(WARMUP_NO_WATER_SIG, column_averages):
      state["overall"] = 'warmup_no_water'
      state["message"] = "Warming up, no water to flush pipes!"
    else:
      state["overall"] = 'other'
      state["message"] = "Not sure what, but something's not right!"
      print "State of flux / flashing detected"
      print "Channel averages: ", all_channel_averages
      print "Column averages: ", column_averages

  return state

  # TODO: CHECK FOR ALL NO BEANS STATES 

  # no more beans = serving light steady + coffee ground light (al fondi) flashing
  # warming up = tazza1 + tazza2 flashing   
  # needs cleaning = descaling light is flashing
  # delivering coffee = single tazza1 or tazza2 light is on
  # currently cleaning = descaling light is on

def test_sig(sig, averages, margin=7.0):
  passed = True
  for i in range(len(sig)):
    diff = abs(averages[i] - sig[i])
    passed = passed & (diff<=margin)
  return passed

def test_steady(averages):
  #is avg steady - ie no flashing
  if abs(max(averages) - min(averages)) <= 1.5:
    return True
  else:
    return False

def test_hi_spread(averages):
  #is there a lot of fluctuation?
  if abs(max(averages) - min(averages)) >= 40:
    return True
  else:
    return False

def test_hival(results):
  #do we have any super high values?
  sample = 0
  while sample < len(results):
    i=0
    while i <= 7:
      if results[sample][i] > 100: 
        return True
      i+=1
    sample+=1
  return False

def collect_readings():
  channel_names      = CHANNEL_NAMES
  channel_readings   = [[],[],[],[],[],[],[],[]]
  channel_averages   = []

  #collect 100 readings for each channel
  x=0
  while x <= 100:
    channel = 0
    while channel <= 7:
      channel_value = readadc(channel, SPICLK, SPIMOSI, SPIMISO, SPICS) # read the analog pin
      channel_value = channel_value / 10.24 # convert 10bit adc0 (0-1024) trim pot read into 0-100 value
      channel_readings[channel].append(channel_value)
      channel+=1
    x+=1
    time.sleep(0.0005)

  #build hash with average from readings for each channel
  channel = 0 
  while channel <= 7:
    channel_average = sum(channel_readings[channel])/len(channel_readings[channel])
    channel_average = round(channel_average, 2)
    channel_averages.append(channel_average)
    channel+=1

  return channel_averages


def press_button(btn):
  #pi gpio pin numbering - refer to rpi3 pin mappings for help
  buttons = { 
    "tazza1": 27,
    "single": 27,
    "tazza2": 17,
    "double": 17,
    "on": 22,
    "onoff": 22,
    "off": 22,
    "vapore": 10,
    "decalcif": 9,
    "premacinato": 11
  }

  pin = buttons[btn]
  print btn+" ", str(pin) 
  if (pin in [17,27,22,10,9,11]):  
    GPIO.output(pin, 1) # set GPIOX to 1/GPIO.HIGH/True
    time.sleep(0.5)
    GPIO.output(pin, 0) # set GPIOX to 0/GPIO.LOW/False
    return True
  else:
    return False
  

def log_results():
  channel_names = CHANNEL_NAMES
  while True: 
    results = collect_readings()
    print time.time(),
    channel = 0
    while channel <= 7:
      #print ",",channel_names[channel], 
      print ",",results[channel],
      if (channel==7):
        print ""
      channel+=1

def log_state():
  while True:
    print "-------------"
    result = read_state()
    print "Result: ", result["overall"]
    time.sleep(0.2)

def cleanup():
  print "Running GPIO.cleanup()"
  GPIO.cleanup()

if __name__ == '__main__': 
  print "Reading board"
  log_state()
