# Dev notes

## Running on startup

Install xautomation

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install xautomation
```


Run the bitbarista scripts on startup by adding a new line to `nano ~/.config/lxsession/LXDE-pi/autostart`. This new line should start with "@" + scriptname (including path to script if necessary): 

So `autostart` should look something like this:

```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@/home/pi/BitBarista/runbitbarista.sh
@/home/pi/BitBarista/runbrowser.sh
```
