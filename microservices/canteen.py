from flask import Flask, jsonify, render_template, request
from datetime import datetime
import logging
import requests
import json
import sys
sys.path.append('../utils')
from Cache import Cache

PORT = 5002
URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"
URL_LOG = "http://127.0.0.1:5006"
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

#TODO: Meter retornos 404 bem


@app.route('/')
def home_page():
    #TODO: adicionar form para meter data?
    return 'Canteen'

@app.route('/<year>/<month>/<day>')
def get_canteen(year, month, day):
    global cache
    try:
        date = day + '/' + month + '/' + year
        data = cache.get(date)
        if data:
            return data

        data = requests.get(url = URL).json()
        for x in data:
            if x["day"] == date:
                cache.put(date, x["meal"])
                return json.dumps(x["meal"])
        return {}
    except:
        return {}

if __name__ == '__main__': 
    global cache
    cache = Cache(7, days=3)
    app.run(port=PORT)