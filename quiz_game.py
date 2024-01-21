import socket
import uuid
import ipaddress
import threading


BROADCAST_PORT = 61424
BUFFER_SIZE = 1024
SUBNETMASK = "255.255.255.0"

IP_ADRESS_OF_THIS_PC = socket.gethostbyname(socket.gethostname())
net = ipaddress.IPv4Network(IP_ADRESS_OF_THIS_PC + '/' + SUBNETMASK, False)
BROADCAST_IP = net.broadcast_address.exploded


class Middleware():
    MY_UUID = str(uuid.uuid4()) 
    def __init__(self, statemashine):
        self.MY_UUID = MY_UUID
        self.statemashine =  statemashine
        self._broadcastHandler = BroadcastHandler()



class BroadcastHandler():
    def __init__(self):


        self._broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listen_socket.bind((IP_ADRESS_OF_THIS_PC, BROADCAST_PORT))
        self._listen_UDP_Broadcast_Thread = threading.Thread(target=self._listenUdpBroadcast)
        self._listen_UDP_Broadcast_Thread.start()

    def broadcast(self, broadcast_message:str):
        self._broadcast_socket.sendto(str.encode(Middleware.MY_UUID +broadcast_message, encoding='utf-8'), (BROADCAST_IP, BROADCAST_PORT))

    def subscribeBroadcastListener(self, observer_func):
        self._listenerList.append(observer_func)
    def _listenUdpBroadcast(self):

            data, addr = self._listen_socket.recvfrom(BUFFER_SIZE)
            if data:
                data = data.decode('utf-8')
                print(data)
                

a = BroadcastHandler()

while True:
     a.broadcast("test2")
     a._listenUdpBroadcast
        


