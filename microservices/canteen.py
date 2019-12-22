from flask import Flask, jsonify
from flask import render_template
from flask import request
import logging
import requests
import json
import sys
sys.path.append('../utils')
from Cache import Cache

PORT = 5002
URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"

#TODO: Meter retornos 404 bem

app = Flask(__name__)

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