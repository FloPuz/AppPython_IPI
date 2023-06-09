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
    """accessing data.db thank to g object and gets all tables"""
    if "db" not in g:
        g.db = sqlite3.connect("data.db")
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Close data base"""
    db = g.pop("db", None)

    if db is not None:
        db.close()

# Init the DB __ But inits each time the app run 
#One could improve the app by looking for the
# db in the path and dont recreate if it already exists
def init_db():
    """Init the Db of the application on ly call once"""
    with app.app_context():
        db = get_db()
    with app.app_context():
        with current_app.open_resource("cheesse.sql") as f:
            db.executescript(f.read().decode("utf8"))

#access login page and check if we are already signed in with session object
@app.route("/")
def login_page():
    """This route is there to redirect you to the login screen on the first connection"""
    init_db()   
    session['login'] = None
    return render_template("login.html")

#render home.html template and if user is none redirects to login page
@app.route("/home")
def home():
    """This is the home, you have acces to the menus there and can navigate"""
    if session['login'] == None:
        return redirect(url_for('login_page'))
    return render_template("home.html")

#if user none going to login page else renders rank page with favorite cheeses
@app.route("/rank")
def rank():
    """A route to load the ranking of the different cheese and show the corresponding  temp"""
    if session['login'] == None:
        return redirect(url_for('login_page'))
    cheeses = get_loved_cheese()
    return render_template("rank.html",cheeses_list=cheeses)

#same logic with no user else renders about-us template
@app.route("/about-us")
def about_us():
    """Load the about us screen"""
    if session['login'] == None:
        return redirect(url_for('login_page'))
    return render_template("about-us.html")


@app.route("/login", methods=["GET", "POST"])
def connection():
    """The method have two parts:
    ------
    if the request is GET checks if user is authenticated else redirecting to login page
    ------
    ------
    taking introduced login and password and checks if user exist and the password is correct.
    Saving user in cookies using session object """
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
        session['idUser'] = user['idUser']
        return redirect(url_for("rank"))


@app.route("/logout")
def log_out():
    """
        Sets user to none and redirects to login page
    """
    session['login'] = None
    return redirect(url_for("connection"))

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    """
    if  method is GET renders to signup page
    else gathers information and checks is user exist. If not registering new user
    and redirects to login page
    """
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

@app.post("/modify_cheese")
def modify_cheese():
    """
    Modifies user's favorite cheese
    """
    login = session['login']
    idUser = session['idUser']
    idCheese = request.form.get('idCheese')
    change_user_cheese(login, idUser, idCheese)
    return redirect(url_for('rank'))

#select all user as a 2D list (ie: user[0]['login'] / user[1]['login'])
def get_all_users():
    """Get all user referenced in the db"""
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    return users
#select all database user as user(ie: user['login']/ user['password'])
def get_user_by_username(login):
    """Ge a specific user thanks to his name in the db"""
    db= get_db()
    user = db.execute('SELECT * FROM user WHERE login = ?',(login,)).fetchone()
    return user

#insert user with user['login']/user['paswword']/user['prenom']
def insert_user(login, password, firstname):
    """Insert a new user in the db, with his name, lastname and password all set up"""
    db= get_db()
    try:
        db.execute(
            "INSERT INTO user (login, password, prenom) VALUES (?, ?, ?)",
            (login, generate_password_hash(password), firstname),
        )
        db.commit()
    except db.IntegrityError:
        error = f"User {login} is already registered."
        return error

#Delete user from DataBase
def delete_user(user):
    """Dele a user in the db using a dic that reprensent him"""
    db= get_db()
    try:
        db.execute("DELETE FROM user WHERE idUser = ?", (user['idUser'] ))
        db.commit()
    except db.IntegrityError:
        error = f"User {user['login']} doesn't exist."
        return error


#Changes the cheese totem from a user even if its outragious 
def change_user_cheese(login, idUser, idCheese):
    """Change the favorite cheese of a user in the db"""
    db = get_db()
    try:
        db.execute("UPDATE user SET idCheese = ? WHERE idUser = ?", (idCheese, idUser), )
        db.commit()
    except db.IntegrityError:
        error = f"User {login} doesn't exist."
        return error

#Get the user 's favorite, hopefully smelly, cheese 
def get_user_cheese(user):
    """Get the favorite cheese of a specific user"""
    db = get_db()
    try:
        cheese = db.execute("SELECT cheese.nom FROM cheese LEFT JOIN user ON user.idUser =?", (user['idUser'])).fetchone()
        return cheese_country[cheese]
    except db.IntegrityError:
        error = f"User {user['login']} doesn't exist."
        return error
     

#Select the most loved cheeses vote
def get_loved_cheese():
    """Get all the loved cheese  [cheese that have been selected by a user]"""
    db = get_db()
    cheeses = db.execute('SELECT *, count(user.idUser) as vote FROM cheese LEFT JOIN user WHERE cheese.idCheese = user.idCheese GROUP BY cheese.idCheese ORDER BY vote DESC').fetchall()
    return cheeses
