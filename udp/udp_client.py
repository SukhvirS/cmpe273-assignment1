import socket
import uuid


UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "ping"

f = open('./upload.txt')
fileData = [line[0:len(line)-1] for line in f.readlines()]

def send(id=0):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ack = int(id)
    for x in fileData:
        randomId = uuid.uuid1()
        correctDataReceived = False
        try:
            # don't send next packet until last correct acknowledgement of last packet is received
            while not correctDataReceived:
                s.sendto(f"{randomId}:{ack}:{x}".encode(), (UDP_IP, UDP_PORT))
                data, ip = s.recvfrom(BUFFER_SIZE)

                dataReceived = data.decode()
                splitData = dataReceived.split(':')
                receivedUUID = splitData[0]
                receivedAck = int(splitData[1])

                if receivedUUID == str(randomId):
                    if receivedAck == ack + 1:
                        if 'pong' in dataReceived:
                            correctDataReceived = True

            # dont sent next package until ack for last package is received
            # while not correctDataReceived:
            #     print('didn\'t receive ack')
            #     s.sendto(f"{id}:{x} (ID: {randomId})".encode(), (UDP_IP, UDP_PORT))
            #     data, ip = s.recvfrom(BUFFER_SIZE)


            # while (receivedUUID != str(randomId)) or (receivedAck != ack + 1) or ('pong' not in data.decode()):
            #     print('didn\'t receive ack')
            #     s.sendto(f"{id}:{x} (ID: {randomId})".encode(), (UDP_IP, UDP_PORT))
            #     data, ip = s.recvfrom(BUFFER_SIZE)

            print("received data: {}: {}".format(ip, data.decode()))
            ack = receivedAck + 1
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()


def get_client_id():
    id = input("Enter client id:")
    return id

send(get_client_id())