from flask import render_template, Flask, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from config import app, login_manager, db
from base import *

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/booking')
def booking():
    return render_template('booking.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        email = request.form['email']
        user_to_add = Users(login=nickname, mail=email)
        try:
            db.session.add(user_to_add)
            db.session.commit()
            login_user(user_to_add, remember=True)
            return redirect('/')
        except:
            message = 'Укажите другую почту или имя пользователя'
            return render_template('register.html', message=message)
    else:
        return render_template('register.html')


@app.route('/login')
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            flash("Вы уже авторизованы")
            return redirect("/")
        return render_template("login.html")
    username = request.form.get('username')
    password = request.form.get('password')
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash('Такого пользователя не существует')
        return redirect("/login")
    if check_password_hash(user.password, password):
        login_user(user)
        return redirect('/')
    else:
        flash('Неверный логин или пароль')
        return redirect('/login')


@app.route('/basket')
def basket():
    return render_template('basket.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/worldviews')
def worldviews():
    return render_template('worldviews.html')

