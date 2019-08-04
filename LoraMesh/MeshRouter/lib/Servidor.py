
import socket
from JsonTraductor import *
import _thread
import pycom
class Servidor:
    #host="192.168.0.40"
    #UDP_IP=host
    #UDP_PORT=10000


    def __init__(self,UDP_IP,UDP_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((UDP_IP,UDP_PORT))
        self.sock.listen(1)

    def conectar(self,mesh):
        print("True o False para Habilitar o deshabilitar" )
        while True:
                print ("Esperando conexión...")
                sc, addr = self.sock.accept()
                print ("Cliente conectado desde: ", addr)
                while True:
                        recibido = sc.recv(4098)
                        jsn=recibido.decode('utf-8')
                        print(jsn)
                        if 'color' in jsn:
                            color=JsonTraductor.convertColorReciv(recibido)
                            numero = int(color)
                            print(numero)
                            print("TENGO QUE ENVIAR :"+ str(numero))
                            mesh.sendAll(JsonTraductor.convertColorSend(color))
        print ("Adios")
        sc.close()
        s.close()
