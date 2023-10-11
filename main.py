from flask import render_template, Flask, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from base import *
from flask import session
from flask_sqlalchemy import SQLAlchemy
from config import adminpass, login_manager
import os


def str_to_int_keys(dict_in):
    cash_ = {}
    for key, val in dict_in.items():
        key = int(key)
        if isinstance(val, dict):
            cash_[key] = str_to_int_keys(val)
        else:
            cash_[key] = val
    return cash_


def check_user():
    if not session.get('admin_version'):
        if current_user.is_authenticated:
            if current_user.admin:
                session['admin_version'] = True
        else:
            session['admin_version'] = False
    return session['admin_version']


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/register')


@app.route('/switch_sort/<type>')
def switch_sort(type):
    if not session.get('sort'):
        session['sort'] = 'rental'
    session['sort'] = type
    return redirect('/booking')


@app.route('/show/<type>/<int:id>')
def show(type, id):
    if type == 'items':
        item = Items.query.get(id)
        if item.active:
            item.active = False
        else:
            item.active = True
    if type == 'rental':
        item = Rental.query.get(id)
        if item.active:
            item.active = False
        else:
            item.active = True
    if type == 'route':
        item = Route.query.get(id)
        if item.active:
            item.active = False
        else:
            item.active = True
    if type == 'locations':
        item = Locate.query.get(id)
        if item.active:
            item.active = False
        else:
            item.active = True
    db.session.commit()
    return redirect(f'/redactor/{type}')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/catalog')
def catalog():
    items = Items.query.filter_by(active=True)
    return render_template('catalog.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/redactor/<mode>')
def redactor(mode):
    if mode == 'rental':
        items = Rental.query.all()
    elif mode == 'route':
        items = Route.query.all()
    elif mode == 'locations':
        items = Locate.query.all()
    else:
        items = Items.query.all()
    return render_template('redactor.html', data=items, mode=mode)


@app.route('/booking')
def booking():
    if not session.get('sort'):
        session['sort'] = 'rental'
    if session.get('sort') == 'rental':
        items = Rental.query.filter_by(active=True)
    elif session.get('sort') == 'route':
        items = Route.query.filter_by(active=True)
    elif session.get('sort') == 'locations':
        items = Locate.query.filter_by(active=True)
    else:
        items = Route.query.filter_by(active=True)
    return render_template('booking.html', data=items)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        email = request.form['email']
        name = request.form['name']
        last_name = request.form['last_name']
        user_to_add = Users(login=nickname, mail=email, name=name, last_name=last_name, bktrip=None, admin=False)
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
    user = Users.query.filter_by(login=username).first()
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
    """if request.method == 'POST':
        for item_id in session['cart'].keys():
            try:
                print(f'count_{item_id}')
                new_count = request.form[f'count_{item_id}']
                session['cart'][item_id] = new_count
                session.modified = True
                break
            except:
                pass
        return redirect('/basket')
    else:
        items_in_cart = []
        if not session.get('cart'):
            session['cart'] = {}

        for item_id in session.get('cart').keys():
            id = int(item_id.split()[0])
            type = item_id.split()[1]
            if type == 'items':
                items_in_cart += [Items.query.get(id)]
            elif type == 'rental':
                items_in_cart += [Rental.query.get(id)]
            elif type == 'route':
                items_in_cart += [Route.query.get(id)]
            elif type == 'locations':
                items_in_cart += [Locate.query.get(id)]
        cart_with_int_keys = str_to_int_keys(session.get('cart'))

        sum_of_items_price = 0
        for item in items_in_cart:
            sum_of_items = item.price * int(cart_with_int_keys.get(item.id))
            sum_of_items_price += int(sum_of_items)

        if items_in_cart:
            payment_button = True
        else:
            payment_button = False"""

    return render_template('basket.html')
    """data=items_in_cart, payment_button=payment_button,
                           dict=cart_with_int_keys, sum_of_items=sum_of_items_price"""


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


@app.route('/delete/<type>/<int:id>')
def delete(type, id):
    if session['admin_version']:
        if type == 'items':
            db.session.delete(Items.query.get(id))
        if type == 'rental':
            db.session.delete(Rental.query.get(id))
        if type == 'route':
            db.session.delete(Route.query.get(id))
        if type == 'locations':
            db.session.delete(Locate.query.get(id))
        db.session.commit()
        return redirect(f'/redactor/{type}')
    else:
        return redirect('/admin')


@app.route('/create/<mode>', methods=['POST', 'GET'])
def create(mode):
    check_user()
    if session['admin_version']:
        if request.method == "POST" and session.get('admin_version'):
            title = request.form['title']
            price = request.form['price']
            img = request.files['img']
            if mode != 'items':
                descript = request.form['descript']
            if mode == 'route':
                locations = request.form['locations']
            else:
                locations = 0
            if img.filename != '':
                if mode == 'items':
                    last_obj = Items.query.order_by(Items.id.desc()).first()
                elif mode == 'locate':
                    last_obj = Locate.query.order_by(Locate.id.desc()).first()
                elif mode == 'route':
                    last_obj = Route.query.order_by(Route.id.desc()).first()
                else:
                    last_obj = Rental.query.order_by(Rental.id.desc()).first()

                if last_obj:
                    last_id = last_obj.id
                    next_id = last_id + 1
                else:
                    next_id = 1
                img_new_filename = f'{img.filename.split(".")[0]}_{next_id}.{img.filename.split(".")[1]}'
                img.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{img_new_filename}'))
                img_track = f'/static/images/{img_new_filename}'

                if mode == 'items':
                    item = Items(name=title, cost=price, img=img_track)
                elif mode == 'locate':
                    item = Locate(name=title, cost=price, img=img_track, descript=descript, active=True)
                elif mode == 'route':
                    item = Route(name=title, cost=price, img=img_track, descript=descript, names=locations, active=True)
                else:
                    item = Rental(name=title, cost=price, img=img_track, descript=descript, active=True)

                try:
                    db.session.add(item)
                    db.session.commit()
                    return redirect('/')
                    # Добать шаблоn с крупной надписью "Товар добавлен в каталог!" и кнопкой "На главную"
                except:
                    return "Ошибака"
            else:
                message = 'Некоректное имя файла'
                return render_template(f'create_{mode}.html', message=message)
        else:
            return render_template(f'create_{mode}.html')
    else:
        return redirect('/admin')


@app.route('/basket/<type>/<int:id>')
def basket_add(type, id):
    if not session.get('cart'):
        session['cart'] = {}
    new_item = {'type': type, 'count': 0}
    session['cart'].setdefault(id, {'type': type, 'count': 0})
    session['cart'][id]['count'] += 1
    session.modified = True
    return f'<script>document.location.href = document.referrer</script>'


if __name__ == '__main__':
    app.run(debug=True)
