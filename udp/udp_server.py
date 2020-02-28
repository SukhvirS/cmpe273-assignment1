import socket


UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "pong"

firstTime = True

def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UDP_PORT))
    print(f'Server started at port {UDP_PORT}')
    global firstTime

    while True:
        data, ip = s.recvfrom(BUFFER_SIZE)

        if firstTime:
            print('Accepting a file upload...')
            firstTime = False

        dataReceived = data.decode(encoding='utf-8').strip()
        splitData = dataReceived.split(':')

        if splitData[0] == 'Done with connection':
            break

        ack = int(splitData[1])
        returnAck = ack + 1

        # format of the data sent to the client: uuid:ack:pong
        MESSAGE = splitData[0]+":"+str(returnAck)+":pong"

        # reply back to the client
        s.sendto(MESSAGE.encode(), ip)
    
    print('Upload successfully completed')
    firstTime = True

listen_forever()