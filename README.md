# BitBarista
An autonomous BTC coffee buying/vending machine.

## Running on startup

Run the bitbarista on startup by adding a new line to `nano ~/.config/lxsession/LXDE-pi/autostart`. This new line should start with "@" + scriptname (including path to script if necessary): 

So `autostart` should look something like this:

```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@/home/pi/BitBarista/runbitbarista.sh
```
