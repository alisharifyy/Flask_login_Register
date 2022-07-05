import os
from datetime import datetime
from flask import Flask, flash, jsonify, redirect ,render_template ,request ,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask_session import Session
from config import Development
from Model import Login ,Register
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
Session(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True ,nullable=False)
    password = db.Column(db.String(128), unique=False ,nullable=False)
    date = db.Column(db.Date(), default=datetime.now())



from functools import wraps
def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



# create db file
if "app.db" not in os.listdir():
    db.create_all()
    print(" * Data Base Created SuccessFully :)")


@app.route("/")
@login_required
def index():
    if not session.get("user_id"):
        return redirect("/login")
    
    # find user name 
    user_info = User.query.filter(User.id == session["user_id"]).first()
    return render_template("index.html",db=user_info)


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "GET":
        form = Login()
        return render_template("login.html",form=form)
    if request.method == "POST":
        form = Login()
        username = request.form.get("username")
        password = request.form.get("password")

        if not username.strip():
            alert = ("username is empty")
            return render_template("login.html",alert=alert, form=form)
        if not password.strip():
            alert = ("password is empty")
            return render_template("login.html",alert=alert, form=form)

        # query to data base for duplicate user
        user_result = User.query.filter_by(username=username).first()
        if not user_result:
            alert = ("information is Wrong")
            return render_template("login.html",alert=alert, form=form)
    
        if user_result.username != username:
            alert = ("Username is Wrong")
            return render_template("login.html",alert=alert, form=form)
        if not check_password_hash(user_result.password,password):
            alert = ("Password is Wrong")
            return render_template("login.html",alert=alert, form=form)
        session["user_id"] = user_result.id
        return redirect("/")


@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "GET":
        form = Register()
        return render_template("register.html",form=form)
    if request.method == "POST":
        register_temp = Register(request.form)
        if not register_temp.validate():
            flash("Invalid Form")
            return redirect(request.url)

        username = request.form.get("username")
        password = request.form.get("password")
        password_re = request.form.get("password_re")
        if not username.strip():
            flash("username is empty")
            return redirect(request.url)
        if not password.strip():
            flash("password is empty")
            return redirect(request.url)
        if not password_re.strip():
            flash("password conformation is empty")
            return redirect(request.url)
        
        if password_re != password:
            flash("Password are Not match")
            return redirect(request.url)

        # query to db to duplicate user
        new_user = User.query.filter(User.username == username).first()  
        if new_user:
            flash("Username already takes by another user")
            return redirect(request.url)

        # add user to db
        new_user_add = User()
        new_user_add.username = username
        new_user_add.password = generate_password_hash(password)

        db.session.add(new_user_add)
        db.session.commit()
        
        flash("Register complete")
        return redirect("/login")

