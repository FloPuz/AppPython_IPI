import sqlite3

from flask import Flask, flash , session
from flask import render_template, redirect, url_for
from flask import request, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret key"

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

# Init the DB __ But inits each time the app run 
#One could improove the app by looking for the 
# db in the path and dont recreate if it already exists
def init_db():
    with app.app_context():
        db = get_db()
    with app.app_context():
        with current_app.open_resource("cheesse.sql") as f:
            db.executescript(f.read().decode("utf8"))

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/rank")
def rank():
    cheeses = get_all_cheeses()
    return render_template("rank.html",cheeses_list=cheeses)

@app.route("/about-us")
def about_us():
    return render_template("about-us.html")


@app.route("/login", methods=["GET", "POST"])
def connection():
    if request.method == "GET":
        if session['login']:
            return render_template("home.html")
        return render_template("login.html")
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        user = get_user_by_username(login)
        if not user or not check_password_hash(user['password'], password):
            flash('Please check your login details and try again.')
            return redirect(url_for("connection"))

        session['login'] = login
        return redirect(url_for("home"))


@app.route("/logout")
def log_out():
    session['login'] = None
    return redirect(url_for("connection"))


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        login = request.form.get('login')
        name = request.form.get('name')
        password = request.form.get('password')
        user = get_user_by_username(login)

        if user:
            flash('Email address already exists')
            session['login'] = None
            return redirect(url_for('connection'))

        insert_user(login , password , name)
        return redirect(url_for('connection'))

# @app.errorhandler(401)
# def access_denied(error):
#     return render_template('access_denied.html'), 401

# @app.errorhandler(404)
# def access_denied(error):
#     return render_template('page_not_found.html'), 404

#select all user as a 2D list (ie: user[0]['login'] / user[1]['login'])
def get_all_users():
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    return users
#select all database user as user(ie: user['login']/ user['password'])
def get_user_by_username(login):
    db= get_db()
    user = db.execute('SELECT * FROM user WHERE login = ?',(login,)).fetchone()
    return user

#insert user with user['login']/user['paswword']/user['prenom']
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

#Delete user from DataBase
def delete_user(user):
    db= get_db()
    try:
        db.execute("DELETE FROM user WHERE idUser = ?", (user['idUser'] ))
        db.commit()
    except db.IntegrityError:
        error = f"User {user['login']} doesn't exist."
        return error


#Changes the cheese totem from a user even if its outragious 
def change_user_cheese(user):
    db = get_db()
    try:
        db.execute("UPDATE FROM user WHERE idUser =? SET idCheese = ?", (user['idUser']), (user['idCheese']))
        db.commit()
    except db.IntegrityError:
        error = f"User {user['login']} doesn't exist."
        return error

#Get the user 's favorite, hopefully smelly, cheese 
def get_user_cheese(user):
    db = get_db()
    try:
        cheese = db.execute("SELECT cheese.nom FROM cheese LEFT JOIN user ON user.idUser =?", (user['idUser'])).fetchone()
        return cheese_country[cheese]
    except db.IntegrityError:
        error = f"User {user['login']} doesn't exist."
        return error
     

#Select the most loved cheeses vote
def get_loved_cheese():
    db = get_db()
    cheeses = db.execute('SELECT *, count(user.idUser) as vote FROM cheese INNER JOIN user ON cheese.idCheese = user.idCheese GROUP BY user.idCheese').fetchone()
    return cheeses

#Get cheeses from bdd
def get_all_cheeses():
    db = get_db()
    cheeses = db .execute('SELECT * FROM cheese').fetchall()
    return cheeses




init_db()