from flask import Flask
from flask import render_template
from flask import request
import logging
import requests
import json

PORT = 5001
URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"

#TODO: Meter retornos 404 bem

app = Flask(__name__)
# logging.basicConfig(filename='../backend/log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s rooms: %(message)s')
# logging.basicConfig(filename='/backend/log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s rooms: %(message)s')

@app.route('/')
def home_page():
    #TODO: adicionar form para meter id?
    return 'Rooms'

@app.route('/<id>')
def get_room(id):
    r = requests.get(url = URL + id)
    data = r.json()
    try:
        if (data.get("description") is not None and data["description"] == "id not found") or data.get("type") != "ROOM":
            return None

        parent = data 

        while parent.get("type") != "BUILDING":
            parent = requests.get(url = URL + parent.get("parentSpace").get("id")).json()

        data["building"] = parent.get("name")
        return data
    except:
        return None

if __name__ == '__main__': 
    app.run(port=PORT)