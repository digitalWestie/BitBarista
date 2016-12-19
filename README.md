# BitBarista
An autonomous BTC coffee buying/vending machine.

## Running on startup

Run the bitbarista on startup by adding a new line to `/etc/xdg/lxsession/LXDE/autostart`. This new line should start with "@" + scriptname (including path to script if necessary): 

So `autostart` should look something like this:

```
@lxpanel --profile LXDE
@pcmanfm --desktop --profile LXDE
@xscreensaver -no-splash
@/home/pi/BitBarista/runbitbarista.sh
```

