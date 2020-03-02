import socket
import sys
import time


TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "ping"

def send():
    args = sys.argv
    id = args[1]
    delay = int(args[2])
    numOfMessages = int(args[3])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(f"Connected Client: {id}".encode())
    data = s.recv(BUFFER_SIZE)


    for i in range(numOfMessages):
        print(f'Sending data: {MESSAGE}')
        s.send(f"{id}:{MESSAGE}".encode())
        data = s.recv(BUFFER_SIZE)
        print(f'Received data: {data.decode()}')
        # no need for delay if sending the last message
        if (i+1) != numOfMessages:
            time.sleep(delay)
    
    s.close()

def get_client_id():
    id = input("Enter client id:")
    return id

# send(get_client_id())
send()
