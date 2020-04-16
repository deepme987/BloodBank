
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient, errors
from hashlib import sha512
from bson import ObjectId
from forms import *

try:
    client = MongoClient("mongodb+srv://Cassie:Cassie@cassie-kdpcc.mongodb.net/"
                         "test?retryWrites=true&w=majority")
    database = client["blood_bank"]
except errors.ServerSelectionTimeoutError:
    print("Cannot connect to mongo server.")
    exit()

app = Flask(__name__)
app.config['SECRET_KEY'] = "lkajdghdadkglajkgah1"


csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user):
        self.user = user
        self.id = user["_id"]
        self.email = user["email"]
        self.name = user["name"]

    def get_id(self):
        return self.email


@login_manager.user_loader
def load_user(user_id):
    for user_info in database["user"].find({"email": user_id}):
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
            flash("User Registered, continue to login")
            return redirect("/login")

    return render_template("newreg.html", form=form)


@app.route("/blooddonated", methods=["POST", "GET"])
@login_required
def donate_blood():
    form = BloodDonateForm()

    if request.method == 'POST':
        database["blood_detail"].insert_one(form.return_data(current_user.id))
        flash("Blood donation request successful, kindly visit nearest center to save someone's life")
        return redirect('/blooddonated')
    return render_template('blooddonated.html', form=form)


@app.route("/view_donations", methods=["POST", "GET"])
@login_required
def view_donations():
    data = database["blood_detail"].find({"id": current_user.id})

    return render_template('view_donations.html', data=data)


@app.route("/changepwd", methods=["POST", "GET"])
@login_required
def change_password():
    userid = current_user.id
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if form.new_password.data != form.confirm_password.data:
            return render_template("changepwd.html", form=form, error="Password and confirm password don't match")

        np = {"$set": {"password": sha512(form.new_password.data.encode()).hexdigest()}}
        for val in database["user"].find({"_id": userid}, {"_id": 0, "password": 1}):
            if val["password"] == sha512(form.old_password.data.encode()).hexdigest():
                database["user"].update_one(val, np)
                flash("Password changed successfully")
                return render_template('changepwd.html', form=form)
            else:
                return render_template("changepwd.html", form=form, error="Invalid old password")

    return render_template('changepwd.html', form=form)


@app.route("/updatepf", methods=["POST", "GET"])
@login_required
def update_profile():
    form = UpdateProfileForm()
    userid = current_user.id

    if form.validate_on_submit():
        val2 = {"$set": {"age": form.age.data, "mobile": form.mobile.data}}
        database["user"].update_one({"_id": userid}, val2)
        flash("Updated Successfully")
        return redirect('/updatepf')

    return render_template('updatepf.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/searchblood", methods=["POST", "GET"])
def searchblood():
    form = SearchBloodForm()

    if form.validate_on_submit():
        data = database["blood_detail"].find({"bg": form.bg.data})
        return render_template("searchblood.html", form=form, data=data)

    return render_template("searchblood.html", form=form, message="No data found")


@app.route("/bloodrequest", methods=["POST", "GET"])
def bloodrequest():
    form = BloodRequestForm()

    if form.validate_on_submit():
        database["blood_request"].insert_one(form.return_data())
        flash("We will get back to you soon.")
        return render_template("bloodrequest.html", form=form)

    return render_template("bloodrequest.html", form=form)


@app.route("/<file>")
def render_file(file):
    return render_template(file + ".html")


if __name__ == '__main__':
    app.run(debug=True)
