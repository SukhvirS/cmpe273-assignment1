import socket
import threading

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def run(self):
        while True:
            data = self.clientSocket.recv(BUFFER_SIZE)
            if not data: 
                # print('No data received.')
                break
            print(f"received data:{data.decode()}")
            self.clientSocket.send("pong".encode())

def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    # conn, addr = s.accept()
    # print(f'Connection address:{addr}')

    while True:
        conn, addr = s.accept()
        newThread = ClientThread(addr, conn)
        newThread.start()
        # print(f'Connection address:{addr}')

        # data = conn.recv(BUFFER_SIZE)
        # if not data: 
        #     print('No data received.')
        #     break
        # print(f"received data:{data.decode()}")
        # conn.send("pong".encode())

    # conn.close()

listen_forever()