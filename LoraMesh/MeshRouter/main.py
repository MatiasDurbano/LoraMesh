#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#
#lopy2
from network import LoRa
import socket
import time
import utime
import ubinascii
import pycom
import machine
import _thread
from lib.Wifi import *
from lib.Servidor import *

from loramesh import Loramesh
from mesh import *



pycom.wifi_on_boot(False)
pycom.heartbeat(False)

#wifi = Wifi("HITRON-92B0","pepe4444")
#wifi = Wifi("IDEI","lagoenelcielo")
#wifi.connect()

lora = LoRa(mode=LoRa.LORA, region=LoRa.US915, tx_power=20,bandwidth=LoRa.BW_125KHZ, sf=12)
#lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868,frequency = 863000000, bandwidth=LoRa.BW_125KHZ, sf=11)
#lora = LoRa(mode=LoRa.LORA, region=LoRa.US915,frequency=903000000,tx_power=19, bandwidth=LoRa.BW_125KHZ, sf=12)
MAC = str(ubinascii.hexlify(lora.mac()))[2:-1]
print("LoRa MAC: %s"%MAC)

#server = Servidor("0.0.0.0",10000)


loram = Loramesh(lora)
mesh= Mesh(loram,MAC,1)
#--------------------------------------------------------------------------------
# waiting until it connected to Mesh network
# se queda intentando conectarse y muestra los vecinos
mesh.connect()
# create UDP socket
#creo un socket LoRa
mesh.createSocket(1234)
# infinite main loop
#funcion principal
#_thread.start_new_thread(server.conectar, (mesh,))
mesh.listen()
