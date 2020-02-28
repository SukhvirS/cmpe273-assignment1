import socket
from socket import timeout
import uuid


UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "ping"
retryCount = 10

f = open('./upload.txt')
fileData = [line[0:len(line)-1] for line in f.readlines()]

def send(id=0):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.2)  # timeout of 20ms

    print('Connected to the server')
    print(f'Starting a file ({f.name}) upload...')

    ack = 1
    for x in fileData:
        randomId = uuid.uuid1()
        count = 0

        while True:
            if count > retryCount:
                break

            try:
                count += 1
                # format of the data sent to server:
                # uuid:ack:data
                s.sendto(f"{randomId}:{ack}:{x}".encode(), (UDP_IP, UDP_PORT))
                data, ip = s.recvfrom(BUFFER_SIZE)

                dataReceived = data.decode()
                splitData = dataReceived.split(':')
                receivedUUID = splitData[0]
                receivedAck = int(splitData[1])

                # only send next packet if correct ack received
                if receivedUUID == str(randomId):
                    if receivedAck == ack + 1:
                        if 'pong' in dataReceived:
                            break

            # retry if server times out
            except timeout:
                print('Server timed out')
                pass

            except socket.error:
                print("Error! {}".format(socket.error))
                pass
        
        if count > retryCount:
            print('Number of attempts exceeded retry limit.')
            break

        # print("received data: {}: {}".format(ip, data.decode()))
        print(f'Received ack({receivedAck}) from the server.')
        ack = receivedAck + 1

    s.sendto(f"Done with connection".encode(), (UDP_IP, UDP_PORT))
    if count <= retryCount:
        print('File upload successfully completed.')

def get_client_id():
    id = input("Enter client id:")
    return id

send(get_client_id())