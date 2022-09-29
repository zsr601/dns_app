from flask import Flask,request
from socket import *
import json

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = int(int(request.args.get('number')))
    if number >=0:
    	return '200, fib({0}) : {1}'.format(number, fib(number))
    else:
    	return '400'

def fib(number):
    if number == 0:
        return 0
    elif number == 1:
        return 1
    else:
        return fib(number - 1) + fib(number - 2)

@app.route('/register', methods=['PUT'])
def register():
    # Parse the input
    temp = request.get_json() 
    hostname,ip,as_ip,as_port = temp['hostname'],temp['ip'],temp['as_ip'],temp['as_port']

    # DNS registration
    sk = socket(AF_INET, SOCK_DGRAM)   
    msg = json.dumps({'TYPE':'A', 'NAME':hostname, 'VALUE': ip, 'TTL': 10 })
    sk.sendto(msg.encode(), (as_ip, 53533))
    msg, _ = sk.recvfrom(2048)
    sk.close()

    # registration is successfull   
    return msg.decode()



app.run(host='0.0.0.0',
        port=9090,
        debug=True)
