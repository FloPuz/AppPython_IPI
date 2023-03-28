from flask import Flask
from flask import render_template, redirect, url_for
from flask import request


app = Flask(__name__)

cheese_country = {
    'Parmigiano Regiano':{
        'flag': 'assets/images/flags/italy.png',
        'photo':'assets/images/cheeses/parmigiano.png',
    },
    'Burrata':{
        'flag': 'assets/images/flags/italy.png',
        'photo':'assets/images/cheeses/burratta.png',
    },
    'Grana Padano':{
        'flag': 'assets/images/flags/italy.png',
        'photo':'assets/images/cheeses/padano.png'
    },
    'Oaxaca cheese':{
        'flag': 'assets/images/flags/mexico.png',
        'photo':'assets/images/cheeses/oaxaca.png'
    },
    'Bundz':{
        'flag': 'assets/images/flags/poland.png',
        'photo':'assets/images/cheeses/bundz.png'
    },
    'Canastra':{
        'flag': 'assets/images/flags/brazil.png',
        'photo':'assets/images/cheeses/canastra.png'
    },
    'Old Amsterdam':{
        'flag': 'assets/images/flags/netherlands.png',
        'photo':'assets/images/cheeses/old_amsterdam.png'
    },
    'Sirene':{
        'flag': 'assets/images/flags/bulgarie.png',
        'photo':'assets/images/cheeses/sirene.png'
    },
    'Graviera Naxou':{
        'flag': 'assets/images/flags/greece.png',
        'photo':'assets/images/cheeses/graviera.png'
    },
    'Sulguni':{
        'flag': 'assets/images/flags/georgia.png',
        'photo':'assets/images/cheeses/sulguni.png'
    },
}

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/rank")
def rank():
    return render_template("rank.html",cheese_country=cheese_country )


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
