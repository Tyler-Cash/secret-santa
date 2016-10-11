import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def login():
    return flask.render_template('login.html')


if __name__ == '__main__':
    app.run()
