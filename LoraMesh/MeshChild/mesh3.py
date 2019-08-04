import time
from network import LoRa
import socket
import time
import utime
import machine
import pycom
from lib.JsonTraductor import *

class Mesh:
    msg = "Hello World! MAC: "

    def __init__(self,Loramesh,MAC,pack_num):
        self.loraMesh=Loramesh
        self.MAC= MAC
        self.pack_num = pack_num
        self.ip = self.loraMesh.ip()

    def connect(self):
        while True:
            self.loraMesh.led_state()
            print("%d: State %s, single %s"%(time.time(), self.loraMesh.cli('state'), self.loraMesh.cli('singleton')))
            time.sleep(2)
            if not self.loraMesh.is_connected():
                print("No conectado")
                continue

            print('Neighbors found: %s'%self.getNeighbors())
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
                    self.socket.sendto('ACK ' + self.MAC + ' ' + str(rcv_data)[2:-1], ('fdde:ad00:beef:0:0:ff:fe00:2000', rcv_port))
                    print("ACK")
                except Exception:
                    pass
            if rcv_data.startswith("ACK"):
                print("ACK RECIBIDO")

    def listen(self):
        while True:
            self.loraMesh.led_state()
            print("%d: State %s, single %s, IP %s"%(time.time(), self.loraMesh.cli('state'), self.loraMesh.cli('singleton'), self.loraMesh.ip()))

            # check if topology changes, maybe RLOC IPv6 changed
            new_ip = self.loraMesh.ip()
            if self.ip != new_ip:
                print("IP changed from: %s to %s"%(self.ip, new_ip))
                self.ip = new_ip

            # update neighbors list
            neigbors = self.loraMesh.neighbors_ip()
            print("%d neighbors, IPv6 list: %s"%(len(neigbors), neigbors))

            # send PING and UDP packets to all neighbors
            for neighbor in neigbors:
                if self.loraMesh.ping(neighbor) > 0:
                    print('Ping OK from neighbor %s'%neighbor)
                    self.loraMesh.blink(10, .1)
                else:
                    print('Ping not received from neighbor %s'%neighbor)

                time.sleep(2)

                self.pack_num = self.pack_num + 1
                try:
                    msg = "Hello World! MAC: " + self.MAC + ", pack: "
                    self.socket.sendto(msg + str(self.pack_num), (neighbor, self.myport))
                    print('Sent message to %s'%(neighbor))
                except Exception:
                    print("revente wachin")
                    pass
                time.sleep(2)

            # random sleep time
            time.sleep(2)
