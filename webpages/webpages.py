from flask import Flask
from flask import render_template
from flask import request
from datetime import *
import json
import requests

#canteenURL="http://127.0.0.1:5002"
#roomURL="http://127.0.0.1:5001"
APIURL="http://192.168.1.81:5004"

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("mainPage.html")

@app.route('/secretariats')
def secretariat_list_page():
    return "sorry"

@app.route('/canteen', methods=['POST'])
def get_canteen_list():
    #s = str(request.form)
    dt = datetime.strptime(request.form["day"], '%Y-%m-%d')
    print(dt.day)
    try:
        url_send = APIURL + '/canteen/' + str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)
        print(url_send)
        data = requests.get(url=url_send).json()
        print(data)
        return render_template("canteenPage.html", day=request.form["day"] , meal=data)
    except Exception as e:
        print(e)
        return render_template("errorPage.html", name="date")

@app.route('/rooms', methods=['POST'])
def rooms_page():
    s = str(request.form)
    value=int(request.form["id"])
    #print(value)
    if value <= 0:
        return render_template("errorPage.html", name="id < 0")
    else:
        try:
            url_send = roomURL + '/' + str(value)
            print(url_send)
            d = requests.gt(url=url_send).json()
            print(d)
            return render_template("roomPage.html", id=request.form["id"], data=d)
        except:
            return render_template("errorPage.html", name="id not valid")

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
    app.run(port=5000)

