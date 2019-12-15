from flask import Flask 
from flask import render_template
from flask import request
from datetime import datetime
import logging
import json
import requests

#canteenURL="http://127.0.0.1:5002"
#roomURL="http://127.0.0.1:5001"
APIURL="http://192.168.1.81:5004"

app = Flask(__name__)
logging.basicConfig(filename='../log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s user-webpages: %(message)s')

@app.route('/')
def hello_world():
    return render_template("mainPage.html")

@app.route('/secretariats')
def secretariat_list_page():
    try:
        send_url = APIURL + '/secretariats'
        data = requests.get(url=send_url).json()
        return render_template("secretariatsPage.html", items=data)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/secretariats/<id>')
def secretariat(id):
    try:
        send_url = APIURL + '/secretariats/' + id
        data = requests.get(url=send_url).json()
        return render_template("secretariatPage.html", info=data)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/canteen', methods=['POST'])
def get_canteen_list():
    dt = datetime.strptime(request.form["day"], '%Y-%m-%d')
    try:
        url_send = APIURL + '/canteen/' + str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)
        data = requests.get(url=url_send).json()
        return render_template("canteenPage.html", day=request.form["day"] , meal=data)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/rooms', methods=['POST'])
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

"""
@app.route('/addValue', methods=['POST'])
def add_Value():
    s = str(request.form)
    if request.form["val"]== None:
        pass
    else:
        val = request.form["val"]
        st.store(val)
    s = st.getSize()
    return hello_world()

@app.route('/value/<key>')
def get_Value(key):
    val = st.getValue(key)
    if val == None:
        return render_template("errorPage.html", name = request.args["key"])
    return str(val)

@app.route('/getValue')
def get_Value2():
    key = str(request.args["key"])
    return get_Value(key)
"""

if __name__ == '__main__':
    app.run(port=5005)

