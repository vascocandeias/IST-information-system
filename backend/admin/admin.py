from flask import Flask 
from flask import render_template
from flask import request
from datetime import datetime
import logging
import json
import requests

class Not200(Exception):
    pass

#canteenURL="http://127.0.0.1:5002"
#roomURL="http://127.0.0.1:5001"
APIURL="http://192.168.1.81:5004"

app = Flask(__name__)
logging.basicConfig(filename='../log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s admin-webpages: %(message)s')

@app.route('/')
def hello_world():
    return render_template("mainPage.html")

@app.route('/logging')
def show_logs():
    l = []
    try:
        f = open("../log.txt", "r")
        l = f.readlines()
        f.close()
        return render_template("logsPage.html", lines=l)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/secretariats', methods=["GET", "POST"])
def secretariat_list_page():
    send_url = APIURL + '/secretariats'
    if request.method=="GET":
        try:
            data = requests.get(url=send_url).json()
            return render_template("secretariatsPage.html", items=data)
        except Exception as e:
            return render_template("errorPage.html", error=str(e))
    elif request.method=="POST":
        try:
            ans = requests.post(url=send_url, data=request.values)
            if ans.status_code!= 200:
                return render_template("errorPage.html", error=str(ans.status_code))
            return render_template("okPage.html")
        except Exception as e:
            return render_template("errorPage.html", error=str(e))

@app.route('/secretariats/<id>', methods=[ "GET", "POST"])
def secretariat(id):
    send_url = APIURL + '/secretariats/' + id
    if request.method=="GET":
        try:
            data = requests.get(url=send_url).json()
            return render_template("secretariatPage.html", info=data)
        except Exception as e:
            return render_template("errorPage.html", error=str(e))
    elif request.method=="POST":
        if request.form["_method"] == "PUT":
            try:
                ans = requests.put(url=send_url, data=request.values)
                if ans.status_code != 200:
                    return render_template("errorPage.html", error=str(ans.status_code))
                return render_template("okPage.html")
            except Exception as e:
                return render_template("errorPage.html", error=str(e))
        elif request.form["_method"]=="DELETE":
            try:
                ans = requests.delete(url=send_url)
                print(ans)
                if ans.status_code != 200:
                    return render_template("errorPage.html", error=str(ans.status_code))
                return render_template("okPage.html")
            except Exception as e:
                return render_template("errorPage.html", error=str(e))   

if __name__ == '__main__':
    app.run(port=5006)


