from flask import Flask,request
from socket import *
from urllib.request import urlopen
import json

app = Flask(__name__)


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    # Parse the parmas
    hostname=request.args.get('hostname')
    fs_port=request.args.get('fs_port')
    number=request.args.get('number')
    as_ip=request.args.get('as_ip')
    as_port=request.args.get('as_port')
    
    # Check all is not None
    if (hostname is None) or (fs_port is None) or (number is None) or (as_ip is None) or (as_port is None):
        return '400'

    # DNS request get the server's ip address
    msg = json.dumps({'TYPE': 'A','NAME': hostname})
    sk = socket(AF_INET, SOCK_DGRAM)
    sk.sendto(msg.encode(), (as_ip, 53533))
    res, _ = sk.recvfrom(2048)
    temp= json.loads(res.decode())
    ip = temp['VALUE']
    sk.close()

    # Access fibonacciServer and get the corresponding fib number.
    return urlopen('http://{0}:{1}/fibonacci?number={2}'.format(ip,fs_port,number)).read()

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
