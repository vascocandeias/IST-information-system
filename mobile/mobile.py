from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import jsonify
import logging
import requests
import json

PORT = 5008
app = Flask(__name__)

dict = {}

@app.route('/')
def mobile():
    username = request.values.get('username')
    print(username)
    global dict
    dict.update({username:1})
    return render_template("appPage.html", )
    

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=PORT)