from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import jsonify
from datetime import datetime
import requests
import json
import pickle

URL_LOG = "http://127.0.0.1:5006"

#TODO: Meter retornos 404 bem

app = Flask(__name__)
filename = 'secretariats.pickle'
PORT = 5005
# cur_id

@app.before_request
def before():
    data = {
        "ip": request.environ.get('REMOTE_ADDR', 'unknown'),
        "time": str(datetime.now()),
        "service": 'secretariats',
        "method": request.method,
        "endpoint": request.path,
        "payload": str(request.data),
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
        # breakpoint()
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
        return jsonify(secretariat)


@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_sectreteriat(id):
    global cur_id
    global secretariats

    secretariat = list(filter(lambda secretariat: secretariat['id'] == int(id), secretariats))
    if secretariat == []:
        return jsonify({})
    secretariat = secretariat[0]
    
    if request.method == 'GET':
        return secretariat
    
    if request.method == 'PUT':
        data = request.values
        for x in data:
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
        # print(secretariats)
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