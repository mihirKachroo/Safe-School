# -*- encoding: utf-8 -*-
"""
License: Commercial
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from os import environ
from sys import exit
from camera import Camera
from config import config_dict
from app import create_app, db
import os
import shutil

from flask import Flask, jsonify, render_template, redirect, request, url_for, Response, send_file

from camera import Camera
import recognize_faces_image
import logging
from pymongo import MongoClient
from datetime import datetime
import base64
from app.home import routes
from app.base import blueprint

get_config_mode = environ.get('APPSEED_CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid APPSEED_CONFIG_MODE environment variable entry.')

app = create_app(config_mode) 
client = MongoClient("mongodb+srv://admin:Empower999@cluster.dyzkm.mongodb.net/student_db?retryWrites=true&w=majority")
db = client.get_database('student_db')
records = db.student_records
camera = None
first = ""
timestamp = ""
@app.route('/graph', methods=['POST'])
def graph():
    print("First Variable" + first)
    fchoice = "y"
    schoice = "u"
    return render_template('cameraview.html', test = "Welcome", text= first, firstpart = "If you are ", secondpart = ", Click the button below to confirm. If you aren't return to the capture tab.", condition = True)

@app.route('/second', methods=['POST'])
def second():
    new_student = {
        'name': first,
        'timestamp': timestamp
    }
    records.insert_one(new_student)
    return render_template('index.html')

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    global first
    jsdata = request.form['javascript_data']
    today = datetime.today()
    global timestamp
    timestamp = today.strftime("%d-%m-%Y %H")
    with open('static/captures/'+timestamp+".png", "wb") as file:
        file.write(base64.b64decode(jsdata[22:]))
    name = str(recognize_faces_image.main('static/captures/'+timestamp+".png"))
    first = name
    print("Name: " + name)
    print('called')
    return name

    
Migrate(app, db)

if __name__ == "__main__":
    app.run()
