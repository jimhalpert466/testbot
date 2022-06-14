from flask import Flask, render_template, request, redirect, make_response, session, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user
import os
import json
import datetime

app = Flask(__name__)
login_manager = LoginManager(app)


app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:Neet2001@localhost:3306/file?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app_root = os.path.dirname(os.path.abspath(__file__))

# DB Model USER
class User(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    login = db.Column(db.String(200), nullable=True)
    fname = db.Column(db.String(200), nullable=True)
    lname = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Boolean(), nullable=True)

if __name__ == '__main__':
    db.create_all()
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, port=5005)
    # Session(app)