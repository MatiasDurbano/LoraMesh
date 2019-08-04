import socket
import time
class Cliente:

    data=''

    def __init__(self,ip,port):
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UDP_IP=ip
        #UDP_IP="10.13.52.236"
        self.UDP_PORT=port
        self.socket_cliente.connect((self.UDP_IP, self.UDP_PORT))

    def sendMessage(self,msg):
        self.socket_cliente.sendto(msg,(self.UDP_IP,self.UDP_PORT))
        print("enviando y esperando respuesta")
        time.sleep(0.2)
        #esto es asqueroso, me fijo si el mensaje ya esta porque el thread ya lo socket_cliente
        if self.data!='':
            return self.data.decode('utf-8')

    def sendUnansweredMessage(self, msg):
        self.socket_cliente.sendto(msg,(self.UDP_IP,self.UDP_PORT))

    def ServerLister(self):
        self.data = self.socket_cliente.recv(4096)
        return self.data.decode('utf-8')

    #limpio la variable data asi me aseguro de que no va a leer el mismo mensaje en la respuesta nfc
    def clearData(self):
        time.sleep(0.2)
        self.data=''

    def closeConnect(self):
        print ("Adios")
        self.socket_cliente.close()
