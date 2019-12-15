from flask import Flask
from flask import render_template
from flask import request
import requests
import json

URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"

#TODO: Meter retornos 404 bem

app = Flask(__name__)

@app.route('/')
def home_page():
    #TODO: adicionar form para meter data?
    return 'Canteen'

@app.route('/<year>/<month>/<day>')
def get_canteen(year, month, day):
    try:
        date = day + '/' + month + '/' + year
        data = requests.get(url = URL).json()
        for x in data:
            if x["day"] == date:
                return json.dumps(x["meal"])
        return None
    except:
        return None

if __name__ == '__main__': 
    app.run(port=5002)