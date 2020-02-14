import socket
import uuid


UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "ping"

f = open('./upload.txt')
fileData = [line[0:len(line)-1] for line in f.readlines()]

def send(id=0):
    for x in fileData:
        randomId = uuid.uuid1()
        try:
            ack = id
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(f"{randomId}:{ack}:{x}".encode(), (UDP_IP, UDP_PORT))
            data, ip = s.recvfrom(BUFFER_SIZE)

            # dont sent next package until ack for last package is received
            while 'pong' not in data.decode():
                print('didn\'t receive ack')
                s.sendto(f"{id}:{x} (ID: {randomId})".encode(), (UDP_IP, UDP_PORT))
                data, ip = s.recvfrom(BUFFER_SIZE)

            print("received data: {}: {}".format(ip, data.decode()))
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()


def get_client_id():
    id = input("Enter client id:")
    return id

send(get_client_id())