# BitBarista

An autonomous BTC coffee buying/vending machine.

## Starting up

Plug in both the Pi and the coffee machine. The Pi doesn't have a switch. The coffee machine does at the back. Once on it should start the BitBarista interface.

### Startup issues

If it's not connected to the wifi it will probably show an error like: 'Oops! It was not possible to show this website'.

To get on the wifi close the full screen browser using the keyboard by pressing F11. Select a wifi network by pressing the wifi symbol at top right.

To launch the interface press 'Try again' on the browser showing the error page. Once the bitbarista home-page is shown press F11 to put the browser into fullscreen mode. 

Alternatively, you can close all windows and launch the interface again by running the startup short-cut called `runbitbarista.sh`. You should be able to find this on the desktop. It should show a prompt, choose 'Execute in terminal'. Once you've done this open the browser and navigate to `http://localhost:5000`. 

## 