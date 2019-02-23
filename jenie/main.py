
from flask import Flask, render_template, jsonify
from .applications.commuter.train import TrainFinder

app = Flask(__name__)


@app.route("/commuter")
def hello():
    trains = TrainFinder('CHM', 'INT').find_data()
    return jsonify([train.output() for train in trains])


@app.route("/")
def hello2():
    return "Hello World 2!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath