from flask import render_template, Flask, request, redirect, flash
#from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from base import *
from flask import session
from flask_sqlalchemy import SQLAlchemy
from config import adminpass
import os


"""def check_user():
    if not session.get('admin_version'):
        if current_user.is_authenticated:
            for admin_id in admins_id:
                if current_user.id == admin_id:
                    session['admin_version'] = True
        else:
            session['admin_version'] = False
    return session['admin_version']"""


"""@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/register')"""


@app.route('/')
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
            #login_user(user_to_add, remember=True)
            return redirect('/')
        except:
            message = 'Укажите другую почту или имя пользователя'
            return render_template('register.html', message=message)
    else:
        return render_template('register.html')


@app.route('/login')
def login():
    """if request.method == "GET":
        if current_user.is_authenticated:
            flash("Вы уже авторизованы")
            return redirect("/")
        return render_template("login.html")"""
    username = request.form.get('username')
    password = request.form.get('password')
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash('Такого пользователя не существует')
        return redirect("/login")
    if check_password_hash(user.password, password):
        #login_user(user)
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


@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if not session.get('admin_version'):
        session['admin_version'] = False
    if request.method == "POST":
        passw = request.form['password']
        if passw == adminpass:
            session['admin_version'] = True
            return render_template('admin.html')
        return redirect('/')
    else:
        if session.get('admin_version'):
            return render_template('admin.html')
        return render_template('password.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST" and session.get('admin_version'):
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        img = request.files['img']
        if img.filename != '':
            last_obj = Items.query.order_by(Items.id.desc()).first()
            if last_obj:
                last_id = last_obj.id
                next_id = last_id + 1
            else:
                next_id = 1
            img_new_filename = f'{img.filename.split(".")[0]}_{next_id}.{img.filename.split(".")[1]}'
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{img_new_filename}'))
            img_track = f'/static/images/{img_new_filename}'
            item = Items(name=title, cost=price, img=img_track)
            try:
                db.session.add(item)
                db.session.commit()
                return redirect('/')
                # Добать шаблоn с крупной надписью "Товар добавлен в каталог!" и кнопкой "На главную"
            except:
                return "Ошибака"
        else:
            message = 'Некоректное имя файла'
            return render_template('create.html', message=message)
    else:
        return render_template('create.html')



if __name__ == '__main__':
    app.run(debug=True)
