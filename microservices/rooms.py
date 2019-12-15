from flask import Flask
from flask import render_template
from flask import request
import requests
import json

PORT = 5001
URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"

#TODO: Meter retornos 404 bem

app = Flask(__name__)

@app.route('/')
def home_page():
    #TODO: adicionar form para meter id?
    return 'Rooms'

@app.route('/<id>')
def get_room(id):
    r = requests.get(url = URL + id)
    data = r.json()
    try:
        if data["description"] == "id not found" or data["type"] != "ROOM":
            return None
        return data
    except:
        return None

if __name__ == '__main__': 
    app.run(port=PORT)