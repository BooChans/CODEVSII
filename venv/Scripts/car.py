from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def hello():
    return '<h1>!</h1>'