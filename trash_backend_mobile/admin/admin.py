from flask import Flask , render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import requests
import pickle
from werkzeug.security import generate_password_hash, check_password_hash

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

APIURL="http://127.0.0.1:5004"

app = Flask(__name__)
db = pickleDB()
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(user_id):
    return db.get_user(int(user_id))

@app.route('/admin')
def index():
    print(current_user.is_authenticated)
    print(current_user.is_active)
    if current_user.is_authenticated:
        print(current_user.username)
        return render_template("mainPage.html", name=current_user.username, login=True)
    else:
        return render_template("mainPage.html", name="", login=False)

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
                    return redirect('/')
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
                return redirect('/')
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
    send_url = APIURL + '/secretariats'
    if request.method=="GET":
        try:
            data = requests.get(url=send_url).json()
            return render_template("secretariatsPage.html", items=data, name=current_user.username)
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
    send_url = APIURL + '/secretariats/' + id
    if request.method=="GET":
        try:
            data = requests.get(url=send_url).json()
            return render_template("secretariatPage.html", info=data)
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
    return redirect('/')

if __name__ == '__main__':
    app.run(port=5006, debug=True)


