from flask import Flask
from flask import render_template, make_response, abort, redirect, url_for
from flask import session, request
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)

cheese_country = {
    'Parmigiano Regiano':'assets/images/flags/italy.png',
    'Burrata':'assets/images/flags/italy.png',
    'Grana Padano':'assets/images/flags/italy.png',
    'Oaxaca cheese':'assets/images/flags/mexico.png',
    'Bundz':'assets/images/flags/poland.png',
    'Canastra':'assets/images/flags/brazil.png',
    'Old Amsterdam':'assets/images/flags/netherlands.png',
    'Sirene':'assets/images/flags/bulgarie.png',
    'Graviera Naxou':'assets/images/flags/greece.png',
    'Sulguni':'assets/images/flags/georgia.png',
}

cheese_photo = {
    'Parmigiano Regiano':'assets/images/cheeses/parmigiano.png',
    'Burrata':'assets/images/cheeses/burratta.png',
    'Grana Padano':'assets/images/cheeses/padano.png',
    'Oaxaca cheese':'assets/images/cheeses/oaxaca.png',
    'Bundz':'assets/images/cheeses/bundz.png',
    'Canastra':'assets/images/cheeses/canastra.png',
    'Old Amsterdam':'assets/images/cheeses/old_amsterdam.png',
    'Sirene':'assets/images/cheeses/sirene.png',
    'Graviera Naxou':'assets/images/cheeses/graviera.png',
    'Sulguni':'assets/images/cheeses/sulguni.png',
}

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/rank")
def rank():

    return render_template("rank.html",cheese_country=cheese_country , cheese_photo=cheese_photo)

@app.route("/rank")
def fromage():
    return render_template("fromage.html")

@app.route("/login", methods=["GET", "POST"])
def connection():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # TODO -- Check in db and add logic
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    # TODO -- remove connection from instance
    return url_for("home")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        print("Handle Logic Please")
        # TODO -- Logic for sign Up


# @app.errorhandler(401)
# def access_denied(error):
#     return render_template('access_denied.html'), 401

# @app.errorhandler(404)
# def access_denied(error):
#     return render_template('page_not_found.html'), 404
