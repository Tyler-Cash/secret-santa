import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def login():
    return flask.render_template('login.html')


@app.route('/login', methods=['POST'])
def check_credentials():
    return flask.render_template('login.html')

if __name__ == '__main__':
    app.run()
