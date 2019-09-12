# pyboard-asnl-results

Display ASNancyLorraine football match results on a tile on a bus on a Pyboard!

![](https://raw.githubusercontent.com/potsky/pyboard-asnl-results/master/image.png)

## Introduction

Here is the result : https://youtu.be/PluuIas89FQ

You can buy parts here :

- 1 [Pyboard D-series](https://store.micropython.org/product/PYBD-SF2-W4F2)
- 1 [MicroPython pyboard D adapter](https://store.micropython.org/product/WBUS-DIP28)
- 1 [Tile 6x6 RGB LED array](https://store.micropython.org/product/TILE-LED36)

## Installation

- Mount the card on your computer
- Edit file `boot.py`
- Change your WiFi credentials
- Save file
- Eject card

## Display logs

To display error logs, launch a serial prompt:

- Windows: you need to go to 'Device manager', right click on the unknown device,
   then update the driver software, using the `pybcdc.inf` file found on this drive.
   Then use a terminal program like Hyperterminal or putty.

- Mac OS X: use the command: `screen /dev/tty.usbmodem*`

- Linux: use the command: `screen /dev/ttyACM0`
