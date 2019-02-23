from flask import Flask, render_template
app = Flask(__name__)


@app.route("/commuter")
def hello():
    return render_template('commuter/train.html')


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