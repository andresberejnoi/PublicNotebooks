# app.py
import os
import pandas as pd
import datetime as dt

from flask import Flask
from flask import render_template
from flask import request, url_for, redirect

from models import db
from models import Cryptocurrency, Transaction

from tools import generate_uri_from_file
#==========================================
database_URI = generate_uri_from_file('db_config.yml')


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database_URI
 
#need secret key for CSRF from WTF-Forms to work
FAKE_SECRET_KEY = 'super_duper_secure_key_1234'   
app.config['SECRET_KEY'] = FAKE_SECRET_KEY
 
# Initialize database and create all tables if they don't exist
db.init_app(app)
with app.app_context():
    db.create_all()
 
@app.route("/",methods=['GET','POST'])
def home():
    return "This is a test"
 
if __name__ == "__main__":
    app.run(port=8000, debug=True)
