from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import jsonify
import logging
import requests
import json

PORT = 5004
app = Flask(__name__)

@app.route('/camera')
def camera():
    return render_template("camera.html")

@app.route('/')
def api():
    # breakpoint()
    print("hey")
    response = jsonify({'var':'value'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=PORT)