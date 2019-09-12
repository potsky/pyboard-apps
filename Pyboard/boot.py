# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import machine
import pyb
import network

#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('VCP+MSC') # act as a serial and a storage device
#pyb.usb_mode('VCP+HID') # act as a serial device and a mouse

pyb.country('FR') # ISO 3166-1 Alpha-2 code, eg US, GB, DE, AU

wl = network.WLAN()
wl.active(1)            # bring up the interface
wl.config(antenna=0)    # select antenna, 0=chip, 1=external
wl.connect('your-ssid', 'Your WiFi Password')  # connect to an access point
#wl.config('mac')        # get the MAC address
#wl.scan()               # scan for access points, returning a list
#wl.isconnected()        # check if connected to an access point
#wl.disconnect()         # disconnect from an access point
