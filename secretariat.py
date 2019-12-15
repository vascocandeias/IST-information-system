from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests
import json
import pickle

#TODO: Meter retornos 404 bem

app = Flask(__name__)
filename = 'secretariat.pickle'

@app.route('/')
def home_page():
    return 'Secretariats'

@app.route('/<id>', methods=['GET', 'POST'])
def get_sectreteriat(id):
    global cur_id
    global secretariats
    try:
        if request.method == 'GET':
            print(secretariats)
            aux = list(filter(lambda secretariat: secretariat['id'] == id, secretariats))
            breakpoint()
            if aux == []:
                return jsonify({})
            return json.dumps(aux[0])
        else:
            secretariat = {}
            secretariat['id'] = cur_id
            cur_id += 1
            secretariat['location'] = request.args.get('location')
            secretariat['name'] = request.args.get('name')
            secretariat['description'] = request.args.get('description')
            secretariat['hours'] = request.args.get('hours')
            secretariats.append(secretariat)
            try:
                f = open(filename, "wb")
                pickle.dump(secretariats, f)
                f.close()
            except Exception as e:
                print(e)
                print("unable to pickle. quitting")
                exit()
            return json.dumps(secretariats)
    except Exception as e:
        print(e)
        return jsonify({})



if __name__ == '__main__': 
    global cur_id
    cur_id = -1
    try:
        f = open(filename, "rb")
        secretariats = pickle.load(f)
        f.close()
        # print(secretariats)
    except FleNotFoundError:
        print("no pickle found. starting fresh")
        secretariats = []
    except Exception as e:
        print(e)
        print("unable to unpickle. quitting.")
        exit()

    for secretariat in secretariats:
        cur_id = secretariat["id"] if secretariat["id"] > cur_id else cur_id

    cur_id += 1
        
    app.run(port=5000)