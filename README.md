# BitBarista

An autonomous BTC coffee buying/vending machine.

## Starting up

Plug in both the Pi and the coffee machine. The Pi doesn't have a switch. The coffee machine does at the back. Once on it should start the BitBarista interface.

### Startup issues

If you see an error like: 'Oops! It was not possible to show this website'. Press the refresh button (or F5). If it's still showing the error, it's likely the Bitbarista is not connected to the wifi.

To get on the wifi close the full screen browser using the keyboard by pressing F11. Select a wifi network by pressing the wifi symbol at top right.

To launch the interface press 'Try again' on the browser showing the error page. Once the bitbarista home-page is shown press F11 to put the browser into fullscreen mode. 

Alternatively, you can close all windows and launch the interface again by running the startup short-cut called `runbitbarista.sh`. You should be able to find this on the desktop. It should show a prompt, choose 'Execute in terminal'. Once you've done this it should open the browser and navigate to `http://localhost:5000`. 

## 