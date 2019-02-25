
from flask import Flask, render_template, jsonify, request
from .applications.commuter.train import TrainFinder

app = Flask(__name__)


@app.route("/commuter")
def commuter():
    """
    Get the latest train times for a route

    E.g - http://127.0.0.1:5000/commuter?departure=CHM&destination=INT
    """
    dept = request.args.get('departure', 'LST')
    dest = request.args.get('destination', 'CHM')
    trains = TrainFinder(dept, dest).find_data()
    return jsonify([train.output() for train in trains])


@app.route("/")
def index():
    return "Hello World!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username
