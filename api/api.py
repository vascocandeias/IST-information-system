from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import jsonify
import requests
import json

PORT = 5004
app = Flask(__name__)
services = {
    'canteen': '127.0.0.1:5002',
    'rooms': '127.0.0.1:5001',
    'secretariat': '127.0.0.1:5000'
}

@app.route('/<service>/<path:subpath>')
def api(service, subpath):
    print(subpath)
    print(services[service])
    aux = redirect(services[service] + '/' + subpath)
    print(aux)
    return aux

if __name__ == '__main__': 
    app.run(port=PORT)