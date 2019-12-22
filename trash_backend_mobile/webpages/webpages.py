from flask import Flask 
from flask import render_template
from flask import request
from datetime import datetime
import logging
import json
import requests

APIURL="http://127.0.0.1:5004"

app = Flask(__name__)

@app.route('/web')
def hello_world():
    return render_template("mainPage.html")

@app.route('/web/secretariats')
def secretariat_list_page():
    try:
        send_url = APIURL + '/secretariats'
        data = requests.get(url=send_url).json()
        return render_template("secretariatsPage.html", items=data)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/web/secretariats/<id>')
def secretariat(id):
    try:
        send_url = APIURL + '/secretariats/' + id
        data = requests.get(url=send_url).json()
        return render_template("secretariatPage.html", info=data)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/web/canteen', methods=['POST'])
def get_canteen_list():
    dt = datetime.strptime(request.form["day"], '%Y-%m-%d')
    try:
        url_send = APIURL + '/canteen/' + str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)
        data = requests.get(url=url_send).json()
        return render_template("canteenPage.html", day=request.form["day"] , meal=data)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/web/rooms', methods=['POST'])
def rooms_page():
    value=int(request.form["id"])
    if value <= 0:
        return render_template("errorPage.html", name="id < 0")
    else:
        try:
            url_send = APIURL + '/rooms/' + str(value)
            d = requests.get(url=url_send).json()
            return render_template("roomPage.html", id=request.form["id"], data=d)
        except Exception as e:
            return render_template("errorPage.html", error=str(e))

if __name__ == '__main__':
    app.run(port=5005)

