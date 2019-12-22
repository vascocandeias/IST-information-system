from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import jsonify
import logging
import requests
import json

PORT = 5009
app = Flask(__name__)

@app.route('/camera')
def camera():
    return render_template("camera.html")

@app.route('/')
def api():
    # breakpoint()
    response = jsonify({'var':'value2'})
    return response

if __name__ == '__main__': 
    app.run(port=PORT)