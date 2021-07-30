from flask import Flask
from flask import render_template
import flask


app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return render_template('index.html')