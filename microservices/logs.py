from flask import Flask, render_template, request, redirect
import json
import requests

PORT = 5006
app = Flask(__name__)

@app.route('/', methods=["POST"])
def add_logs():
    string = request.values.get('ip') + ' ' + request.values.get('time') + " " + request.values.get('service') + " " + request.values.get('method') + " " + request.values.get("endpoint") + " payload: " + request.values.get("payload")
    with open("log.txt", "a") as myfile:
        myfile.write(string + "\n")
    return

if __name__ == '__main__': 
    app.run(port=PORT)   