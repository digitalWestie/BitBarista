# BitBarista

An autonomous BTC coffee buying/vending machine.

## Starting up

### Power on the BitBarista

Plug in both the Pi and the coffee machine. Turn on the coffee machine power switch at the back. The Pi has no power switch and just needs to be plugged in. Once turned on, the screen should show the BitBarista interface in a full-screen browser window.

### 'Oops! It was not possible to show this website'

If you see a page with this error, press the browser refresh button or F5. If you still see the same message, make sure the BitBarista has an active Wifi connection.

### Connect to Wifi

To connect to a wifi network first exit the full-screen browser mode (by pressing F11). A menu bar should now be visible at the top of the screen. Select a wifi network by pressing the wifi symbol at the top right.

Once connected, test the wifi connection by opening a browser window. Do this by clicking the world and cursor icon on the left side of the menu bar or using the drop-down: `Menu -> Internet -> Epiphany Web Browser`. You will need to take this step if the wifi connection requires a web login.

Once the browser is open try navigating to a website using the address bar and pressing `Enter`. If this works, navigate to the BitBarista home page by entering `http://localhost:5000/` in the browser's address bar. 

### Restarting the BitBarista Interface

Navigate to the desktop by closing all windows (by either tapping the window's 'X' button or pressing Alt+F4). 

Launch the interface again by running the startup short-cut found on the desktop called `runbitbarista.sh`. Execute the shortcut by double-tapping or selecting it and pressing `Enter`. 

It should show a prompt, choose 'Execute in terminal'. Once you've done this the script should run the BitBarista application and open a browser window showing the BitBarista interface. Once the interface is showing press F11 to put the browser into fullscreen mode.
