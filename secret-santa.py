import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return flask.render_template('base.html')


if __name__ == '__main__':
    app.run()
