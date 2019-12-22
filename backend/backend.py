from flask import Flask, render_template, request, redirect, jsonify, url_for, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import secrets
import logging
import requests
import json
import pickle

################# Global variables
PORT = 5000
APIURL = "http://127.0.0.1:" + str(PORT) + "/API"
app = Flask(__name__)


################# API variables
services = {
    'canteen': 'http://127.0.0.1:5002',
    'rooms': 'http://127.0.0.1:5001',
    'secretariats': 'http://127.0.0.1:5005'
}

################# Authentication variables 
redirect_uri = "http://127.0.0.1:5000/userAuth" # this is the address of the page on this app 
client_id= "570015174623374" # copy value from the app registration
clientSecret = "FlO1nGCmmV+KtaTFRMyoJtNMMZZpZSD4zme+cNHfq4mDQEXFbJqSzJBhgtEdZ2tbYK01JhyIKyzfatUXkd02PA==" # copy value from the app registration 
fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
tokensDict = {}
secretsDict = {}
requestsDict = {}

################# Admin variables 
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/amdin/login'
SECRETARIAT_URL = APIURL + "/secretariats"
# to use API POST, PUT and DELETE, comment line below
SECRETARIAT_URL = services["secretariats"]


########################################### Mobile app ########################################### 
@app.route('/mobile', methods = ["GET", "POST"])
def private_page(secret = ""):
    if tokensDict.get(request.cookies.get("token")) == None:
        redPage = fenixLoginpage % (client_id, redirect_uri)
        return redirect(redPage)

    return render_template("privPage.html", token = request.values.get("secret"))

@app.route('/userAuth')
def userAuthenticated():
    #This page is accessed when the user is authenticated by the fenix login pagesetup

    #first we get the secret code retuner by the FENIX login
    code = request.args['code']

    # we now retrieve a fenix access token
    payload = {
        'client_id': client_id,
        'client_secret': clientSecret,
        'redirect_uri' : redirect_uri,
        'code' : code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(fenixacesstokenpage, params = payload)
    if(response.status_code == 200):
        #if we receive the token
        r_token = response.json()

        secret = secrets.token_urlsafe()

        global tokensDict
        while tokensDict.get(secret):
            secret = secrets.token_urlsafe()
        
        # we store it
        tokensDict.update({secret:r_token['access_token']})

        #now the user has done the login
        response = make_response(redirect('/mobile'))
        response.set_cookie('token', secret)
        return response
    else:
        return 'oops 1'


@app.route('/mobile/camera', methods=["GET", "POST"])
def camera():
    if tokensDict.get(request.cookies.get("token")) == None:
        redPage = fenixLoginpage % (client_id, redirect_uri)
        return redirect(redPage)

    return render_template("camera.html")
    

@app.route('/mobile/id', methods=["GET", "POST"])
def id():
    if tokensDict.get(request.cookies.get("token")) == None:
        redPage = fenixLoginpage % (client_id, redirect_uri)
        return redirect(redPage)

    userToken = tokensDict.get(request.cookies.get("token"))
    params = {'access_token': userToken}
    resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

    if (resp.status_code == 200):
        r_info = resp.json()
        user = {
            "photo":r_info.get("photo"),
            "name":r_info.get("name"),
            "istid":r_info.get("username")        
        }
        return render_template("secret.html", user=user)
    else:
        return "oops"

@app.route('/mobile/requests/<secret>')
def ping(secret):
    if tokensDict.get(request.cookies.get("token")) == None:
        redPage = fenixLoginpage % (client_id, redirect_uri)
        return redirect(redPage)
    try:
        global requestsDict
        userToken = requestsDict.pop(secret)
        params = {'access_token': userToken}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

        if (resp.status_code == 200):
            r_info = resp.json()
            user = {
                "photo":r_info.get("photo"),
                "name":r_info.get("name"),
                "istid":r_info.get("username")        
            }
            return user
        else:
            return {}, 404
    except:
        if secretsDict.get(secret):
            return {}, 404
        return {}, 410
    
@app.route('/mobile/secret', methods=["POST", "GET"])
def getSecret():
    if tokensDict.get(request.cookies.get("token")) == None:
        redPage = fenixLoginpage % (client_id, redirect_uri)
        return redirect(redPage)

    global secretsDict
    if request.method == "POST":
        secret = secrets.token_urlsafe(5)
        while secretsDict.get(secret):
            secret = secrets.token_urlsafe()
        
        secretsDict.update({secret:tokensDict.get(request.cookies.get("token"))})
        return {"secret":secret}
    
    if request.method == "GET":
        secret = request.values["secret"]
        token = secretsDict.pop(secret)
        global requestsDict
        requestsDict.update({secret:tokensDict.get(request.cookies.get("token"))})
        params = {'access_token': token}
        r_info = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params).json()
        user = {
            "photo":r_info.get("photo"),
            "name":r_info.get("name"),
            "istid":r_info.get("username")        
        }
        return user
        
@app.route('/mobile/logout')
def user_lougout():
    response = make_response(redirect("https://id.tecnico.ulisboa.pt/cas/logout"))
    response.set_cookie('token', '', expires=0)
    return response


############################################### API ############################################### 
# @app.route('/API/<service>', defaults={'subpath': ''}, methods=['GET', 'POST'])
# @app.route('/API/<service>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# To use API for POST, PUT and DELETE methods, uncomment two lines above and comment line bellow
@app.route('/API/<service>', defaults={'subpath': ''}, methods=['GET'])
@app.route('/API/<service>/<path:subpath>', methods=['GET'])
def api(service, subpath):
    try:
        url = services[service] + '/' + subpath
    except:
        return {}, 404
    if request.method == 'GET':
        aux = requests.get(url).json()
    elif request.method == 'POST':
        aux = requests.post(url, data = request.values).json()
    elif request.method == 'PUT':
        aux = requests.put(url, data = request.values).json()
    elif request.method == 'DELETE':
        aux = requests.delete(url).json()
    return json.dumps(aux)
    

############################################## Admin #############################################
class user(UserMixin):
    def __init__(self, id, username, email, hashed_password):
        self.id=id
        self.username=username
        self.email=email
        self.password=hashed_password
    
    def does_password_match(self, password):
        if check_password_hash(self.password, password):
            return True
        else:
            return False

class pickleDB:
    def __init__(self):
        self.id=0
        self.filename="db.pickle"
        try:
            f = open(self.filename, 'rb')
            self.users = pickle.load(f)
            f.close()
        except FileNotFoundError:
            print("no pickle found. starting fresh")
            self.users= []
        except Exception as e:
            print(e)
            print("unable to unpickle. quitting.")
            exit()

    def add_new(self, username, email, password):
        self.id=self.id+1
        hashed_password = generate_password_hash(password, method='sha256')
        u = user(self.id, username, email, hashed_password)
        self.users.append(u)
        f=open(self.filename, 'wb')
        pickle.dump(self.users, f)
        f.close()
    
    def does_user_exist(self, username):
        for u in self.users:
            if u.username==username:
                return True
        return False

    def login(self, username, password):
        for u in self.users:
            if u.username==username:
                if u.does_password_match(password):
                    return u
                else:
                    return None
        return None
    
    def get_user(self, user_id):
        for u in self.users:
            if u.id==user_id:
                return u
        return None

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

db = pickleDB()

@login_manager.user_loader
def load_user(user_id):
    return db.get_user(int(user_id))

@app.route('/admin')
def index():
    if current_user.is_authenticated:
        return render_template("mainPageAdmin.html", name=current_user.username, login=True)
    else:
        return render_template("mainPageAdmin.html", name="", login=False)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if request.method == 'GET':
            return render_template("login.html", form=form)
        elif request.method == 'POST':
            if form.validate_on_submit():
                usr = db.login(form.username.data, form.password.data)
                
                if usr is not None:
                    login_user(usr, remember=form.remember.data)
                    return redirect('/admin')
                else:
                    return render_template("errorPage.html", error="invalid password or username")
            return render_template("errorPage.html", error="invalid form submited")
    except Exception as e:
        return render_template("errorPage.html", error=str(e))


@app.route('/admin/signup', methods=["GET", "POST"])
def signup():
    try:
        form = RegisterForm()
        if form.validate_on_submit():
            if db.does_user_exist(form.username.data) == False:
                db.add_new(form.username.data, form.email.data, form.password.data)
                return redirect('/admin')
            return render_template("errorPage.html", error="user already exists")
        return render_template('signup.html', form=form)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/admin/logging')
@login_required
def show_logs():
    l = []
    try:
        f = open("../log.txt", "r")
        l = f.readlines()
        f.close()
        return render_template("logsPage.html", lines=l, name=current_user.username)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))


@app.route('/admin/secretariats', methods=["GET", "POST"])
@login_required
def secretariat_list_page():
    send_url = SECRETARIAT_URL
    if request.method=="GET":
        try:
            data = requests.get(url=send_url).json()
            return render_template("secretariatsPageAdmin.html", items=data, name=current_user.username)
        except Exception as e:
            return render_template("errorPage.html", error=str(e))
    elif request.method=="POST":
        try:
            ans = requests.post(url=send_url, data=request.values)
            if ans.status_code!= 200:
                return render_template("errorPage.html", error=str(ans.status_code))
            return render_template("okPage.html")
        except Exception as e:
            return render_template("errorPage.html", error=str(e))

@app.route('/admin/secretariats/<id>', methods=[ "GET", "POST"])
@login_required
def secretariat(id):
    send_url = SECRETARIAT_URL + '/' + id
    if request.method=="GET":
        try:
            data = requests.get(url=send_url).json()
            return render_template("secretariatPageAdmin.html", info=data)
        except Exception as e:
            return render_template("errorPage.html", error=str(e))
    elif request.method=="POST":
        if request.form["_method"] == "PUT":
            try:
                ans = requests.put(url=send_url, data=request.values)
                if ans.status_code != 200:
                    return render_template("errorPage.html", error=str(ans.status_code))
                return render_template("okPage.html")
            except Exception as e:
                return render_template("errorPage.html", error=str(e))
        elif request.form["_method"]=="DELETE":
            try:
                ans = requests.delete(url=send_url)
                print(ans)
                if ans.status_code != 200:
                    return render_template("errorPage.html", error=str(ans.status_code))
                return render_template("okPage.html")
            except Exception as e:
                return render_template("errorPage.html", error=str(e))   

@app.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect('/admin')

############################################ Webpages ############################################
@app.route('/web')
def hello_world():
    return render_template("mainPageWeb.html")

@app.route('/web/secretariats')
def web_secretariat_list_page():
    try:
        send_url = APIURL + '/secretariats'
        data = requests.get(url=send_url).json()
        return render_template("secretariatsPageWeb.html", items=data)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/web/secretariats/<id>')
def web_secretariat(id):
    try:
        send_url = APIURL + '/secretariats/' + id
        data = requests.get(url=send_url).json()
        return render_template("secretariatPageWeb.html", info=data)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/web/canteen', methods=['POST'])
def get_canteen_list():
    dt = datetime.strptime(request.form["day"], '%Y-%m-%d')
    try:
        url_send = APIURL + '/canteen/' + str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)
        data = requests.get(url=url_send).json()
        return render_template("canteenPage.html", day=request.form["day"] , meal=data)
    except Exception as e:
        return render_template("errorPage.html", error=str(e))

@app.route('/web/rooms', methods=['POST'])
def rooms_page():
    value=int(request.form["id"])
    if value <= 0:
        return render_template("errorPage.html", name="id < 0")
    else:
        try:
            url_send = APIURL + '/rooms/' + str(value)
            d = requests.get(url=url_send).json()
            return render_template("roomPage.html", id=request.form["id"], data=d)
        except Exception as e:
            return render_template("errorPage.html", error=str(e))


############################################ Main app ############################################
if __name__ == '__main__': 
    app.run(port=PORT)