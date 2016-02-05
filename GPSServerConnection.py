import socket
import struct

class GPSServerConnection:

    def __init__(self):
        self.portA = 9090;
        self.portB = 9091;
        self.ipA = '194.47.3.240';
        self.sendSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sendSock.settimeout(1)
        self.recvSock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.recvSock.settimeout(1)
        self.recvSock.bind(("",self.portB))


    def getPosition(self,robotID):
        try:
            message=struct.pack('!HHH',robotID,69,30)
            self.sendSock.sendto(message, (self.ipA, self.portA))
            data= self.recvSock.recv(2)
            id=struct.unpack('!H',data)[0]
            data= self.recvSock.recv(2)
            posX=struct.unpack('!H',data)[0]
            data= self.recvSock.recv(2)
            posY=struct.unpack('!H',data)[0]
            data= self.recvSock.recv(8)
            pictureTime=struct.unpack('!d',data)[0]
            data= self.recvSock.recv(8)
            currentTime=struct.unpack('!d',data)[0]
            if posX==65535 or posY==65535:
                print "Out of sight"
                return (None,None)
            else:
                return ((posX,posY),pictureTime)
        except socket.timeout:
            print "Timed out"
            return (None,None)
