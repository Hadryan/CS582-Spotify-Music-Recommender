
# imports

import time
import redis
from flask import Flask, render_template, url_for, json
from flask import request, redirect, flash, jsonify, make_response, Response
import os, sys
import random
import string
import datetime
import requests
import logging
import json
from dotenv import load_dotenv

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# Home page, show the demographic music
@app.route('/', methods=['GET'])
@app.route('//', methods=['GET'])
def showHome():
     if request.method == 'GET':
        token = getSpoitfyClientToken()
        allTracks = getSpoitfyTracks(token)
        return render_template("index.html", allTracks = allTracks)




def getSpoitfyClientToken(): 
   # call spotify get token api
   auth_response =  requests.post("https://accounts.spotify.com/api/token", {
    'grant_type': 'client_credentials',
    'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
    'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
    })
    # convert response to json
   auth_response_data = auth_response.json()
   # get the token
   access_token = auth_response_data['access_token']
   return access_token



def getSpoitfyTracks(token): 
   # read the tracks ids file
   text_file = open("cachedData/popularity_sorted_tracks_ids.txt", "r")
   tracksIds = text_file.readlines()

   headers = {'Authorization': 'Bearer ' + token}
   BASE_URL = 'https://api.spotify.com/v1/'

   data = []

   for trackId in tracksIds:
      if(len(trackId) == 23):
         trackId = trackId[:-1]

      auth_response = requests.get(BASE_URL + 'tracks/' + trackId, headers=headers)
      auth_response_data = auth_response.json()

      # add track name and image into list of pairs
      print( auth_response_data['album']['name'],file=sys.stderr)
      data.append(tuple([auth_response_data['name'], auth_response_data['album']['images'][0]['url']]))

   return data


@app.route('/content')
def my_form():
    return render_template('content.html')

@app.route('/content', methods=['POST'])
def my_form_post():
    input_nopol = request.form['text_box']
    if request.method == 'POST':
       with open('nopol.txt', 'w') as f:
            f.write(str(input_nopol))
    return render_template('content.html', nopol=input_nopol)



if __name__ == '__main__':
    app.run(debug=True)