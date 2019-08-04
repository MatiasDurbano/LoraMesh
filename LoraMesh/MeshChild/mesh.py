import time
import socket
import time
import utime
import machine
import pycom
import _thread
import os
from network import LoRa
from lib.JsonTraductor import *

class Mesh:
    msg = "Hello World! MAC: "
    packEnviado=0
    packRecib=0
    simulacion=0
    metros=24
    escrituraActiva=True
    iniciarPrueba=True

    def __init__(self,Loramesh,MAC,pack_num):
        self.loraMesh=Loramesh
        self.MAC= MAC
        self.pack_num = pack_num
        self.ip = self.loraMesh.ip()
        self.loraMesh.setState(0)


    def connect(self):
        while True:
            self.loraMesh.led_state()
            print("STATE:", self.loraMesh.cli('state'))
            print("%d: State %s, single %s"%(time.time(), self.loraMesh.cli('state'), self.loraMesh.cli('singleton')))
            time.sleep(2)
            if not self.loraMesh.is_connected():
                print("No conectado")
                continue

            print('Neighbors found: %s'%self.getNeighbors())
            #creo el archivo
            self.f=open('sim.txt','w')
            self.f.write("(rx_timestamp, rssi, snr, sftx, sfrx, tx_trials, tx_power, tx_time_on_air, tx_counter, tx_frequency)\r\n")
            for t in self.loraMesh.lora.stats():
                self.f.write(("%s, ")%t)
            self.f.write("\r\n")
            self.f.close()
            break

    def getNeighbors(self):
        neighbors=self.loraMesh.neighbors()
        print(print('Neighbors found: %s'%neighbors))
        return neighbors

    def createSocket(self,port):
        self.sockets = []
        self.socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.myport=port
        self.socket.bind(port)
        self.sockets.append(self.socket)
        self.loraMesh.mesh.rx_cb(self.receive_pack,self.sockets)

    def receive_pack(self,sockets):
        # listen for incomming packets
        while True:
            rcv_data, rcv_addr = self.socket.recvfrom(128)
            if len(rcv_data) == 0:
                break
            rcv_ip = rcv_addr[0]
            rcv_port = rcv_addr[1]
            print('Incomming %d bytes from %s (port %d)'%(len(rcv_data), rcv_ip, rcv_port))
            print(rcv_data)
            # could send some ACK pack:
            if rcv_data.startswith("Hello"):
                try:
                    self.socket.sendto('ACK ' + self.MAC + ' ' + str(rcv_data)[2:-1], (rcv_ip, rcv_port))
                    print("ACK ENVIADO")
                except Exception:
                    pass
            if rcv_data.startswith("ACK"):
                print("ME LLEGO UN ACK")
                self.packRecib +=1
            #else:
            #    color=JsonTraductor.convertColorReciv(rcv_data)
            #    numero = int(color)
            #    print(numero)
            #    pycom.rgbled(numero)
            #    try:
            #        self.socket.sendto('received ' + self.MAC + ' ' + str(rcv_data)[2:-1], (rcv_ip, rcv_port))
            #    except Exception:
            #        pass
            #    time.sleep(2)
            #self.loraMesh.blink(7, .3)

    def listen(self):
        while True:
            self.f=open("sim.txt","a+")
            #self.loraMesh.led_state()
            self.iniciarPrueba=True
            print("%d: State %s, single %s, IP %s"%(time.time(), self.loraMesh.cli('state'), self.loraMesh.cli('singleton'), self.loraMesh.ip()))
            # check if topology changes, maybe RLOC IPv6 changed
            new_ip = self.loraMesh.ip()
            if self.ip != new_ip:
                print("IP changed from: %s to %s"%(self.ip, new_ip))
                self.ip = new_ip

            # update neighbors list
            self.neig=self.loraMesh.neighbors()
            neigbors = self.loraMesh.neighbors_ip()
            print("%d neighbors, IPv6 list: %s"%(len(neigbors), neigbors))
            print("------------------------------------")
            print("rssi: ",self.neig)
            #print(self.loraMesh.cli("router 0xe800"))
            print("------------------------------------")
            # send PING and UDP packets to all neighbors
            if(len(neigbors)==0):
                pycom.rgbled(0x080808)
            for neighbor in neigbors:
                pycom.rgbled(0x000400)
                if self.loraMesh.ping(neighbor) > 0:
                    print('Ping OK from neighbor %s'%neighbor)
                    #self.packRecib+=1
                    #self.loraMesh.blink(10, .1)
                else:
                    print('Ping not received from neighbor %s'%neighbor)

                #for b in range(0,20):
                for i in range (0,20):
                    self.pack_num = self.pack_num + 1
                    try:
                        msg = "Hello World! MAC: " + self.MAC + ", pack: "
                        self.socket.sendto(msg + str(self.pack_num), (neighbor, self.myport))
                        self.packEnviado += 1
                        print('Sent message to %s'%(neighbor))

                    except Exception:
                        print("revente wachin")
                        pass
                    time.sleep(4)

            time.sleep(10)
                # random sleep time
            #time.sleep(60)
            self.escribir()
            pycom.rgbled(0x000004)
            print("ya puede cerrar")
            time.sleep(40)


    def escribir(self):
        if self.escrituraActiva:
            print("escribiendo")
            pycom.rgbled(0x000400)
            #ahora deberia escribirlo en un txt
            self.f.write("simulacion %d"%self.simulacion )#," , paquetes enviados :",self.packEnviado ," paquetes recibidos: ",self.packRecib)
            self.f.write("\r\n")
            self.f.write("distancia: %d "%(self.simulacion*self.metros))
            self.f.write("datos de nodo vecino:  %s"%self.neig)
            self.f.write("\r\n")
            self.f.write(" paquetes enviados %d"%self.packEnviado)
            self.f.write(" paquetes recibidos %d\r\n"%self.packRecib)
                #reset de variables
            print("ya guardado")
            self.f.close()
            self.simulacion +=1
            self.packEnviado=0
            self.packRecib=0
