from flask import Flask, render_template, request, redirect
from datetime import datetime
# from werkzeug.datastructures import CombinedMultiDict
import requests
import json
import pickle

URL_LOG = "http://127.0.0.1:5006"

#TODO: Meter retornos 404 bem

app = Flask(__name__)
filename = 'secretariats.pickle'
PORT = 5005

@app.before_request
def before():
    data = {
        "ip": request.environ.get('REMOTE_ADDR', 'unknown'),
        "time": str(datetime.now()),
        "service": app.name,
        "method": request.method,
        "endpoint": request.path,
        "payload": str(request.values.to_dict(flat=True)),
        }
    requests.post(URL_LOG, data = data)

@app.route('/', methods=['GET','POST'])
def home_page():
    global cur_id
    global secretariats

    if request.method == 'GET':
        return json.dumps(secretariats) 
    else:
        secretariat = {}
        secretariat['id'] = cur_id
        cur_id += 1
        data = request.values
        secretariat['location'] = data.get('location')
        secretariat['name'] = data.get('name')
        secretariat['description'] = data.get('description')
        secretariat['hours'] = data.get('hours')
        secretariat['type'] = "SECRETARIAT"
        secretariats.append(secretariat)
        try:
            f = open(filename, "wb")
            pickle.dump(secretariats, f)
            f.close()
        except Exception as e:
            print(e)
            print("unable to pickle. quitting")
            exit()
        return secretariat


@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_sectreteriat(id):
    global cur_id
    global secretariats

    try:
        secretariat = list(filter(lambda secretariat: secretariat['id'] == int(id), secretariats))
    except:
        secretariat = []

    if secretariat == []:
        return {}
        
    secretariat = secretariat[0]
    
    if request.method == 'GET':
        return secretariat
    
    if request.method == 'PUT':
        data = request.values
        for x in data:
            if x in secretariat:
                aux = {x: data[x]}
                secretariat.update(aux)
        try:
            f = open(filename, "wb")
            pickle.dump(secretariats, f)
            f.close()
        except Exception as e:
            print(e)
            print("unable to pickle. quitting")
            exit()
        return secretariat
    
    if request.method == 'DELETE':
        secretariats.remove(secretariat)
        try:
            f = open(filename, "wb")
            pickle.dump(secretariats, f)
            f.close()
        except Exception as e:
            print(e)
            print("unable to pickle. quitting")
            exit()
        return {'status': 'ok'}

if __name__ == '__main__': 
    global cur_id
    cur_id = -1
    
    try:
        f = open(filename, "rb")
        secretariats = pickle.load(f)
        f.close()
    except FileNotFoundError:
        print("no pickle found. starting fresh")
        secretariats = []
    except Exception as e:
        print(e)
        print("unable to unpickle. quitting.")
        exit()

    for secretariat in secretariats:
        cur_id = secretariat["id"] if secretariat["id"] > cur_id else cur_id
    cur_id += 1
        
    app.run(port=PORT)