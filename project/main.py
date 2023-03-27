from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/rank')
def rank():
    return render_template('rank.html')
