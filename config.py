import datetime
from flask import Flask, render_template, request, redirect
#from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

#login_manager = LoginManager(app)
#login_manager.login_view = 'authorization'
