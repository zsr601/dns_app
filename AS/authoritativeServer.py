from socket import *
import json

# Open the socket
sk = socket(AF_INET, SOCK_DGRAM)
sk.bind(('', 53533))

# Waiting for requests
while True:
    msg, ip = sk.recvfrom(2048)
    temp = json.loads(msg.decode())
    length = len(temp)

    if length == 4:  # add autho
        with open('temp.txt', 'w') as of:
            json.dump(temp, of)
            msg = '201'
    elif length == 2:  # check auoth
        with open("temp.txt", 'r', encoding='utf-8') as of:
            for line in of.readlines():
                row = json.loads(line)
                if temp['TYPE'] == row['TYPE'] and temp['NAME'] == row['NAME']:
                    msg = json.dumps(row)
                else:
                    msg = 'ERROR'
    else:
        msg ='ERROR'

    sk.sendto(msg.encode(), ip)

