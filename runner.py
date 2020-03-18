
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient, errors
from hashlib import sha512
from bson import ObjectId
from forms import *


try:
    client = MongoClient("mongodb://localhost:27017/")
    database = client["blood_bank"]
except errors.ServerSelectionTimeoutError:
    print("Cannot connect to mongo server.")
    exit()

app = Flask(__name__)
app.config['SECRET_KEY'] = "lkajdghdadkglajkgah"

csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user):
        self.id = user["_id"]
        self.email = user["email"]
        self.name = user["name"]

    def get(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    for user_info in database["user"].find({"_id": ObjectId(user_id)}):
        user = User(user_info)
        return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    form = LoginForm()
    return render_template('login.html', form=form, error="You need to login to continue")


@app.route("/")
@app.route("/home")
def redirect_index():
    return redirect("/index")


@app.route('/login', methods=["POST", "GET"])
def login_handle():
    form = LoginForm()

    # if form.validate_on_submit():
    if request.method == "POST":
        user_flag = True
        for val in database["user"].find({"email": form.email.data}):
            user_flag = False
            if val["password"] == sha512(form.password.data.encode()).hexdigest():
                user = User(val)
                login_user(user)
                return redirect('/dfg2')
            else:
                return render_template('login.html', form=form, error="Invalid credentials")
        if user_flag:
            return render_template('login.html', form=form, error="No such user found")
    return render_template('login.html', form=form)


@app.route("/newreg", methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            form.password.data = sha512(form.password.data.encode()).hexdigest()
            database["user"].insert_one(form.data)
            return redirect("/login")

    return render_template("/newreg.html", form=form)


@app.route("/blooddonated", methods=["POST", "GET"])
@login_required
def donate_blood():
    return render_template('blooddonated.html')


@app.route("/changepwd", methods=["POST", "GET"])
@login_required
def change_password():
    return render_template('changepwd.html', message="Password changed successfully")


@app.route("/updatepf", methods=["POST", "GET"])
@login_required
def update_profile():
    form = RegisterForm()
    return render_template('updatepf.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/<file>")
def render_file(file):
    return render_template(file + ".html")


if __name__ == '__main__':
    app.run(debug=True)
