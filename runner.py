
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def redirect_index():
    return redirect("/index")


@app.route("/newreg", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        pass

    return render_template("newreg.html")


@app.route("/<file>")
def render_file(file):
    return render_template(file + ".html")


if __name__ == '__main__':
    app.run(debug=True)
