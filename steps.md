steps.md

### Rotating the touchscreen

Added `lcd_rotate=2` to `/boot/config.txt`

### Using remote desktop

On pi:

`sudo apt-get install xrdp`
`ifconfig` (to get ip address)

On laptop: 

`sudo apt-get install rdesktop`
`rdesktop 192.168.0.41`

### Setting up flask

`sudo apt-get update` (general update)

Installing Flask: 

```
sudo apt-get install python-virtualenv -y
sudo pip install --upgrade pip
sudo pip install Flask
```

### Using Electrum

Install dependencies: 

`sudo apt-get install python-qt4 python-pip`

Install: 

`sudo pip install https://download.electrum.org/2.6.3/Electrum-2.6.3.tar.gz`

