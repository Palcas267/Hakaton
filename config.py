import datetime
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'error123'
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'dbilders@mail.ru'
app.config['MAIL_PASSWORD'] = 'uhgCR7sSEHmeepN7dZRJ'

adminpass = 'error123'

login_manager = LoginManager(app)
login_manager.login_view = 'authorization'
