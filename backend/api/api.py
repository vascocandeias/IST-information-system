from flask import Flask, render_template, request, redirect, jsonify, url_for
import secrets
import logging
import requests
import json

PORT = 5000

services = {
    'canteen': 'http://127.0.0.1:5002',
    'rooms': 'http://127.0.0.1:5001',
    'secretariats': 'http://127.0.0.1:5005'
}

redirect_uri = "http://127.0.0.1:5000/userAuth" # this is the address of the page on this app

client_id= "570015174623374" # copy value from the app registration
clientSecret = "FlO1nGCmmV+KtaTFRMyoJtNMMZZpZSD4zme+cNHfq4mDQEXFbJqSzJBhgtEdZ2tbYK01JhyIKyzfatUXkd02PA==" # copy value from the app registration

fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

dict = {}
secretsDict = {}
app = Flask(__name__)

@app.route('/users')
def get_users():
    return dict

@app.route('/mobile', methods = ["GET", "POST"])
def private_page(secret = ""):
    #this page can only be accessed by a authenticated username
    userToken = dict.get(request.values.get("secret"))

    if userToken == None:
        #if the user is not authenticated
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)

    #if the user ir authenticated
    #we can use the userToken to access the fenix

    return render_template("privPage.html", token = request.values.get("secret"))

    # params = {'access_token': userToken}
    # resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

    # if (resp.status_code == 200):
    #     r_info = resp.json()
    #     # print( r_info)
    #     return render_template("privPage.html", username=loginName, name=r_info['name'])
    # else:
    #     return "oops"

@app.route('/userAuth')
def userAuthenticated():
    #This page is accessed when the user is authenticated by the fenix login pagesetup

    #first we get the secret code retuner by the FENIX login
    code = request.args['code']

    # we now retrieve a fenix access token
    payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
    response = requests.post(fenixacesstokenpage, params = payload)
    if(response.status_code == 200):
        #if we receive the token
        r_token = response.json()

        secret = secrets.token_urlsafe()

        global dict
        while dict.get(secret):
            secret = secrets.token_urlsafe()
        
        # we store it
        dict.update({secret:r_token['access_token']})
        # breakpoint()

        #now the user has done the login
        return redirect(url_for("private_page", secret = secret))
    else:
        return 'oops 1'


@app.route('/mobile/camera', methods=["GET", "POST"])
def camera():
    return render_template("camera.html")
    

@app.route('/mobile/id', methods=["GET", "POST"])
def id():
    user = {"photo":"https://www.w3schools.com/images/w3schools_green.jpg", "name":"NAME", "istid":"425496"}
    return render_template("secret.html", user=user)
    
@app.route('/mobile/secret', methods=["POST", "GET"])
def getSecret():
    global secretsDict
    # print("Secret: " + request.values.get("secret"))
    # breakpoint()
    if request.method == "POST":
        secret = secrets.token_urlsafe(5)
        while secretsDict.get(secret):
            secret = secrets.token_urlsafe()
        
        secretsDict.update({secret:dict.get(request.values.get("secret"))})
        print(secretsDict)
        return {"secret":secret}
    
    if request.method == "GET":
        secret = request.values["secret"]
        print(request.values)
        token = secretsDict.pop(secret)
        params = {'access_token': token}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        print(resp.json())
        return resp.json()
        

@app.route('/APi/<service>', defaults={'subpath': ''}, methods=['GET', 'POST'])
@app.route('/API/<service>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api(service, subpath):
    # breakpoint()
    try:
        url = services[service] + '/' + subpath
    except:
        return {}
    if request.method == 'GET':
        aux = requests.get(url).json()
    elif request.method == 'POST':
        aux = requests.post(url, data = request.values).json()
    elif request.method == 'PUT':
        aux = requests.put(url, data = request.values).json()
    elif request.method == 'DELETE':
        aux = requests.delete(url).json()
    return json.dumps(aux)
    
if __name__ == '__main__': 
    app.run(port=PORT)