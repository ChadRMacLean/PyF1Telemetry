import socket

class CMSocket:

    CM_SERVER = { "IP": "127.0.0.1", "PORT": 20777 }

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock.bind((self.CM_SERVER["IP"], self.CM_SERVER["PORT"]))

    def recv(self, size):
        data, addr = self.sock.recvfrom(size)
        if data: 
            return data
            