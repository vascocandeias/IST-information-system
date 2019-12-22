from flask import Flask, render_template, request
from datetime import datetime
import logging
import requests
import json
import sys
sys.path.append('../utils')
from Cache import Cache

PORT = 5001
URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"
URL_LOG = "http://127.0.0.1:5006"
#TODO: Meter retornos 404 bem

app = Flask(__name__)

@app.before_request
def before():
    data = {
        "ip": request.environ.get('REMOTE_ADDR', 'unknown'),
        "time": str(datetime.now()),
        "service": app.name,
        "method": request.method,
        "endpoint": request.path,
        "payload": str(request.values.to_dict(flat=True)),
        }
    requests.post(URL_LOG, data = data)

@app.route('/')
def home_page():
    #TODO: adicionar form para meter id?
    return 'Rooms'

@app.route('/<id>')
def get_room(id):

    global cache
    data = cache.get(id)

    if data:
        return data

    r = requests.get(url = URL + id)
    try:
        data = r.json()
        if (data.get("description") is not None and data["description"] == "id not found") or data.get("type") != "ROOM":
            return {}

        parent = data 

        while parent.get("type") != "BUILDING":
            parent = requests.get(url = URL + parent.get("parentSpace").get("id")).json()

        data["building"] = parent.get("name")

        cache.put(id, data)
        return data
    except:
        return {}

if __name__ == '__main__': 
    global cache
    cache = Cache(100, days=1)
    app.run(port=PORT)