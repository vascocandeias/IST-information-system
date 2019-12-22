from flask import Flask, render_template, request, redirect, send_from_directory
import json
import requests

PORT = 5006
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def add_logs():
    if request.method == "POST":
        string = request.values.get('ip') + ' ' + request.values.get('time') + " " + request.values.get('service') + " " + request.values.get('method') + " " + request.values.get("endpoint") + " payload: " + request.values.get("payload")
        with open("static/log.txt", "a") as myfile:
            myfile.write("\t" + string + "\n")
        return {}
    
    return send_from_directory('static/', filename="log.txt")

if __name__ == '__main__': 
    app.run(port=PORT)