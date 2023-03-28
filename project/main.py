import sqlite3

from flask import Flask
from flask import render_template, make_response, abort, redirect, url_for
from flask import session, request, current_app, g
from markupsafe import escape
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash


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

# db logic code
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("data.db")
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
    with app.app_context():
        with current_app.open_resource("cheesse.sql") as f:
            print("ok")
            db.executescript(f.read().decode("utf8"))           

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
def log_out():
    # TODO -- remove connection from instance
    return  redirect(url_for("connection"))


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

#récupère tous les users sous la forme de tableau 2D (ie: user[0]['login'] / user[1]['login'])
def get_all_users():
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    return users
#récupère un utilsiateur donnée sous forme de user (ie: user['login']/ user['password'])
def get_user_by_username(login):
    db= get_db()
    user = db.execute('SELECT * FROM user WHERE login = ?',(login,)).fetchone()
    if user is not None:
        return user

#insère un utilisateur avec user['login']/user['paswword']/user['prenom']
def insert_user(login, password, prenom):
    db= get_db()
    try:
        db.execute(
            "INSERT INTO user (login, password, prenom) VALUES (?, ?, ?)",
            (login, generate_password_hash(password), prenom),
        )
        db.commit()
    except db.IntegrityError:
        error = f"User {login} is already registered."
        return error

#Supprime un user de la db
def delete_user(user):
    db= get_db()
    try:
        db.execute("DELETE FROM user WHERE idUser = ?", (user['idUser'] ))
        db.commit()
    except db.IntegrityError:
        error = f"User {user['login']} doesn't exist."
        return error
    
#Get all cheese of a specific user and order them by ranking
def get_cheese_by_user(user):
    db= get_db()
    try:
        result = db.execute("SELECT user.prenom ,cheese.nom , userCheese.rank from cheese INNER JOIN user INNER JOIN userCheese ON userCheese.idUser = ? ORDER BY userCheese.rank", (user['idUser'] ))
        cheeses = result.fetchall()
        return cheeses
        
    except db.IntegrityError:
        error = f"User {user['login']} doesn't exist."
        return error















