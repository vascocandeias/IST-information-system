from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import jsonify
import logging
import requests
import json

PORT = 5004
app = Flask(__name__)
# logging.basicConfig(filename='../log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s api: %(message)s')
# logging.basicConfig(filename='backend/log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s api: %(message)s')
services = {
    'canteen': 'http://127.0.0.1:5002',
    'rooms': 'http://127.0.0.1:5001',
    'secretariats': 'http://127.0.0.1:5005'
}

@app.route('/camera')
def camera():
    return render_template("camera.html")
    
@app.route('/<service>', defaults={'subpath': ''}, methods=['GET', 'POST'])
@app.route('/<service>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api(service, subpath):
    # breakpoint()
    try:
        url = services[service] + '/' + subpath
    except:
        return {}
    if request.method == 'GET':
        aux = requests.get(url).json()
    elif request.method == 'POST':
        # breakpoint()
        aux = requests.post(url, data = request.values).json()
    elif request.method == 'PUT':
        aux = requests.put(url, data = request.values).json()
    elif request.method == 'DELETE':
        aux = requests.delete(url).json()
    # aux.headers.add('access-control-allow-origin', '*')
    # aux.headers.add('access-control-allow-headers', 'content-type,authorization')
    # aux.headers.add('access-control-allow-methods', 'get,put,post,delete,options')
    return json.dumps(aux)

if __name__ == '__main__': 
    app.run(port=PORT)