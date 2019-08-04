import network
import machine
from network import WLAN
import time
#
# Set up WLAN
#
class Wifi:

    wlan = WLAN(mode=WLAN.STA) # get current object, without changing the mode

    def __init__(self,ssid,key):
        self.ssid=ssid
        self.key=key

    def connect(self):
        nets = self.wlan.scan()
        for net in nets:
            if net.ssid == self.ssid:
                print('Network found!')
                print(self.ssid+ "  "+self.key)
                self.wlan.connect(net.ssid, auth=(WLAN.WPA2, self.key), timeout=5000)
                while not self.wlan.isconnected():
                    machine.idle() # save power while waiting
                print('WLAN connection succeeded!')
                print(self.wlan.ifconfig())
                break
    def isconnected(self):
        return self.wlan.isconnected()

    def set(self):
        if not wlan.isconnected():
            connect(self)
#set()
#
# Set up server
#
#print("ejecutado")
