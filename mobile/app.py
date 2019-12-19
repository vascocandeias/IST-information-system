from flask import Flask, redirect, render_template, request, jsonify, url_for
import secrets
import requests

#to get the following value go to:
# FENIX -> Pessoal - Gerir Aplicações -> criar
#https://fenixedu.org/dev/tutorials/use-fenixedu-api-in-your-application/ (Step1)

redirect_uri = "http://127.0.0.1:5000/userAuth" # this is the address of the page on this app

client_id= "570015174623374" # copy value from the app registration
clientSecret = "FlO1nGCmmV+KtaTFRMyoJtNMMZZpZSD4zme+cNHfq4mDQEXFbJqSzJBhgtEdZ2tbYK01JhyIKyzfatUXkd02PA==" # copy value from the app registration

fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

loginName = False
userToken = None
code = False
dict = {}
app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return render_template("appPage.html", username=loginName)

@app.route('/users')
def get_users():
    return dict

@app.route('/', methods = ["GET", "POST"])
def private_page(secret = ""):
    #this page can only be accessed by a authenticated username
    userToken = dict.get(request.values.get("secret"))

    if userToken == None:
        #if the user is not authenticated
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)

    #if the user ir authenticated
    # print(userToken)

    #we can use the userToken to access the fenix

    # Meter aqui a nossa app: página para aceder ao qrcode ou personal info

    return render_template("privPage.html", token = userToken)

    params = {'access_token': userToken}
    resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

    if (resp.status_code == 200):
        r_info = resp.json()
        # print( r_info)
        return render_template("privPage.html", username=loginName, name=r_info['name'])
    else:
        return "oops"

@app.route('/userAuth')
def userAuthenticated():
    #This page is accessed when the user is authenticated by the fenix login pagesetup

    #first we get the secret code retuner by the FENIX login
    code = request.args['code']
    # print ("code "+request.args['code'])


    # we now retrieve a fenix access token
    payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
    response = requests.post(fenixacesstokenpage, params = payload)
    # print (response.url)
    # print (response.status_code)
    if(response.status_code == 200):
        #if we receive the token
        r_token = response.json()

        secret = secrets.token_urlsafe()

        global dict
        while dict.get(secret):
            secret = secrets.token_urlsafe()
        
        # we store it
        dict.update({secret:r_token['access_token']})

        #now the user has done the login
        # return jsonify(r_info)
        #we show the returned infomration
        #but we could redirect the user to the private page
        print("Before")
        # requests.post('ttp://127.0.0.1:5000/', data = {"secret": secret})
        return redirect(url_for("private_page", secret = secret))
        # print("After")
        # return requests.post('http://127.0.0.1:5000/', data = {"secret": secret}) #comment the return jsonify....
    else:
        return 'oops 1'

if __name__ == '__main__':
    app.run()