from flask import redirect, request, Flask
#from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from config import db, app


class Users(db.Model, ):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False, default='Пользователь')
    last_name = db.Column(db.String, nullable=False, default='Пользователь')
    mail = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=0)
    bktrip = db.Column(db.Integer)

    def __init__(self, login, name, last_name, mail, admin, bktrip):
        self.login = login
        self.name = name
        self.last_name = last_name
        self.mail = mail
        self.admin = admin
        self.bktrip = bktrip

    def __str__(self):
        return "ID: {}, Логин: {}, Имя: {}, Фамилия: {}, Почта: {}, admin: {}, Бронирование: {}".format(self.id, self.login, self.name, self.last_name, self.mail, self.admin, self.bktrip)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def __str__(self):
        return "ID: {}, Товар: {}, Цена: {}".format(self.id, self.name, self.cost)


class Locate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def __str__(self):
        return "ID: {}, Товар: {}, Цена: {}".format(self.id, self.name, self.cost)


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    def __init__(self, names, name, cost):
        self.names = names
        self.name = name
        self.cost = cost

    def __str__(self):
        return "ID: {}, Места: {}, Название маршрута: {}, Цена: {}".format(self.id, self.names, self.name, self.cost)


def Print(list):
    for e in list:
        print(e)


with app.app_context():
    db.create_all()
    #db.session.add(Users("Катя", 13, 15300))
    #db.session.add_all([])# добавить список объектов в бд
    #db.session.commit()  # сохрание изменений


