# Developer Notes


### Switching on instruction page

Press here to ready the machine. Please wait a moment while the machine heats up and the pipes are flushed. 

Present an intermediate page for duration of heat up.

Once done, bounce to start page. 


### Water refill

Offer a choice of free coffee or collecting BTC

### Grinds clearing

Offer a choice of free coffee or collecting BTC, if we have time offer an ignore button

### Beans refill / no beans scenario

serve-coffee:

  if served fine, go to refill-payout
  if no beans detected, go to beans-refill

beans-refill: 

  show instructions: 

    1. Your last payment has been refunded
    2. Please refill the container (done)  
    3. I'm ready to serve a free coffee (press here to serve)
  
  If successful go to start.


### Possible beans refill / no beans scenario

serve-coffee:

  if served fine, go to refill-payout
  if no beans detected, go to beans-refill

refill-payout:
  
  settle payments to any owed refill payouts  
  clear any saved refill payouts
  go to start page

beans-refill: 

  show instructions:  

    1. refill beans container image (next)
    2. scan your address for a payout (scan)
    3. thanks, your address will be credited upon the next sale of coffee! (done)

  wait for scan, once we have an address, save it
  on done, go to start
