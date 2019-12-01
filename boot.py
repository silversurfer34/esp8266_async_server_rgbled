try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

access_point = False
station = None

if access_point:
    #Access point
    ssid = 'xxx'
    password = 'yyy'
    station = network.WLAN(network.AP_IF)
    station.active(True)
    station.config(essid=ssid, password=password)
    while not station.active():
        print("access point not active")
        pass
else:
    #Connect to router
    ssid = 'xxx'
    password = 'yyy'
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected():
      pass


print('Connection successful')
print(station.ifconfig())

led = Pin(5, Pin.OUT)
