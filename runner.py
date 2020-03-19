
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient, errors
from hashlib import sha512
from bson import ObjectId
from forms import *


try:
    client = MongoClient("mongodb://localhost:27018/")
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
    form = BloodDonateForm()

    if(request.method == 'POST'):
        database["blood_detail"].insert_one(form.data)
        return redirect('/dfg2')
    return render_template('blooddonated.html', form = form)


@app.route("/changepwd", methods=["POST", "GET"])
@login_required
def change_password():
    userid = current_user.id
    form = ChangePasswordForm()

    if(request.method == 'POST'):
        np = { "$set" : {"password": sha512(form.new_password.data.encode()).hexdigest() }}
        for val in database["user"].find({"_id": userid}, {"_id":0, "password":1}):
            if ( val["password"] == sha512(form.old_password.data.encode()).hexdigest() ):
                database["user"].update_one(val, np)
                return render_template('changepwd.html', form=form, message="Password changed successfully")
    return render_template('changepwd.html', form=form, error = "Some error occured")


@app.route("/updatepf", methods=["POST", "GET"])
@login_required
def update_profile():
    form = UpdateProfileForm()
    userid = current_user.id

    if(request.method == 'POST'):
        val2 = { "$set" : {"name":form.name.data, "gender":form.gendre.data, "age":form.age.data, "mobile":form.mobile.data}}
        for val in database["user"].find({"_id":userid}, {"_id":0, "name":1, "gender":1, "age":1, "mobile":1}):
            database["user"].update_one(val, val2)
            return redirect('/updatepf')
    return render_template('updatepf.html', form = form, message = "Some error occurred")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/searchblood", methods=["POST", "GET"])
def searchblood():
    form = SearchBloodForm()

    if(request.method == 'POST'):
        for val in database["blood_detail"].find({"bg":form.bg.data}, {"_id":0, "NoOfUnits":1}):
            print(val) #show data in table format & redirect to bloodrequest.html (blood-request-form)
            return render_template("/searchblood.html", form=form, message = "data found")
    return render_template("/searchblood.html", form=form, message = "No data found")


@app.route("/bloodrequest", methods=["POST", "GET"])
def bloodrequest():
    form = BloodRequestForm()

    if(request.method == 'POST'):
        database["blood_request"].insert_one(form.data)
        return render_template("/bloodrequest.html", form=form, message = "We will get back to you soon...")
    return render_template("/bloodrequest.html", form=form, message = "Some error occured")

@app.route("/<file>")
def render_file(file):
    return render_template(file + ".html")


if __name__ == '__main__':
    app.run(debug=True)
