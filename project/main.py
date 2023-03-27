from flask import Flask
from flask import render_template, make_response, abort, redirect, url_for
from flask import session, request
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/rank')
def rank():
    return render_template('rank.html')

@app.route('/login')
def connection():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('login.html')

@app.errorhandler(401)
def access_denied(error):
    return render_template('access_denied.html'), 401

@app.errorhandler(404)
def access_denied(error):
    return render_template('page_not_found.html'), 404

