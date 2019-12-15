from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import jsonify
import logging
import requests
import json

PORT = 5004
app = Flask(__name__)
logging.basicConfig(filename='../log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s api: %(message)s')
services = {
    'canteen': 'http://127.0.0.1:5002',
    'rooms': 'http://127.0.0.1:5001',
    'secretariat': 'http://127.0.0.1:5000'
}

@app.route('/<service>/<path:subpath>')
def api(service, subpath):
    try:
        url = services[service] + '/' + subpath
    except:
        return {}
    if request.method == 'GET':
        aux = requests.get(url).json()
    elif request.method == 'POST':
        aux = requests.post(url).json()
    elif request.method == 'PUT':
        aux = requests.put(url).json()
    elif request.method == 'DELETE':
        aux = requests.delete(url).json()
    return json.dumps(aux)

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=PORT)