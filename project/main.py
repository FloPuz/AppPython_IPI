from flask import Flask, flash
from flask import render_template, make_response, abort, redirect, url_for
from flask import session, request
from markupsafe import escape
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from project import get_db

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/rank")
def rank():
    return render_template("rank.html")


@app.route("/login", methods=["GET", "POST"])
def connection():
    if request.method == "GET":
        return render_template("login.html")
    else:
        if request.method == 'POST':
            login = request.form['login']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE login = ?', (login,)
        ).fetchone()

        if user is None:
            error = 'Incorrect login.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
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
