import socket


UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "pong"

def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UDP_PORT))

    while True:
        # get the data sent to us
        data, ip = s.recvfrom(BUFFER_SIZE)
        dataReceived = data.decode(encoding='utf-8').strip()
        splitData = dataReceived.split(':')

        ack = int(splitData[1])
        print("{}: {}".format(ip, dataReceived))

        returnAck = ack + 1
        MESSAGE = splitData[0]+":"+str(returnAck)+":pong"

        # reply back to the client
        s.sendto(MESSAGE.encode(), ip)

listen_forever()