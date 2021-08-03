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

# Dempgraphic API
@app.route('/', methods=['GET'])
def showDemographic():
     if request.method == 'GET':
        token = getSpoitfyClientToken()
        allTracks = getSpoitfyTracks(token, 'cachedData/popularity_sorted_tracks_ids.txt')
        print(allTracks,file=sys.stderr)
        print(type(allTracks),file=sys.stderr)
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


def getSpoitfyTracks(token, path): 

   # read the tracks ids file
   text_file = open(path, "r")
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
      data.append(trackId)

   return data



# Content based API
@app.route('/content')
def addContent():
    return render_template('content.html')

@app.route('/content', methods=['POST'])
def addContentPost():
    trackName = request.form['text_box']
    if request.method == 'POST':
       with open('track.txt', 'w') as f:
            f.write(str(trackName))
    allTracks = showContentBased()
    return render_template("index.html", allTracks = allTracks)


def showContentBased():
  # read from track file which we have submited inside the track we need similiar to
  with open('track.txt', 'r') as file:
    track = file.read().replace('\n', '')
  # read from contnt based cached file to find that track name
  my_csv = open('cachedData/content_based_names.csv')
  tracks = []
  for line in my_csv:
    str1=line.split(',')
    if track in str1:
       tracks =line
       break
  list = tracks.split(",") 
  list.pop(0) 
  print(list,file=sys.stderr)
  print(type(list),file=sys.stderr)
  return list



# Collaborative API
@app.route('/collaborative')
def addCollaborative():
    return render_template('collaborative.html')

@app.route('/collaborative', methods=['POST'])
def addollaborativePost():
    userID = request.form['text_box']
    if request.method == 'POST':
       with open('id.txt', 'w') as f:
            f.write(str(userID))
    allTracks = showCollaborative()
    return render_template("index.html", allTracks = allTracks)


def showCollaborative():
  with open('id.txt', 'r') as file:
    id = file.read().replace('\n', '')
  my_csv = open('cachedData/SVG_Track_Names.csv')
  tracks = []
  for line in my_csv:
    str1=line.split(',')
    if id in str1:
       tracks =line
       break
  list = tracks.split(",") 
  list.pop(0) 
  print(list,file=sys.stderr)
  print(type(list),file=sys.stderr)
  return list



if __name__ == '__main__':
    app.run(debug=True)