from flask import Flask, url_for, abort, redirect
from flask import request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

@app.get('/user/query')
def query():
    filter = request.args.get('filter', '')
    return f'{filter}\'s query'

@app.post('/login')
def login_post():
    json = request.get_json(False)
    email = json['email']
    return {
        "email": email,
        "login": "OK",
    }

@app.route('/redirect')
def redir():
    return redirect(url_for('hello_world'))

@app.route('/abort')
def login():
    abort(401)
