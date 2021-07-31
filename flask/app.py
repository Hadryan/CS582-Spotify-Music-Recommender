
# imports
import time

import redis
from flask import Flask, render_template, url_for, json
from flask import request, redirect, flash, jsonify, make_response
from model import *
import os, sys
import random
import string
import datetime
import httplib2
import requests


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# Home page, show the demographic music
@app.route('/', methods=['GET'])
@app.route('/home/', methods=['GET'])
def showHome():
     if request.method == 'GET':
        allTracks = 
        return render_template("index.html", allTracks = allTracks)
