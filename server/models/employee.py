# coding=utf-8
from app import db


class EmployeeInfo(db.Model):
    __tablename__ = 'employee_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ORG_ID = db.Column(db.Integer)
    CLIENT_ID = db.Column(db.Integer)
    username = db.Column(db.String(50), info='用户名')
    gender = db.Column(db.String(5), info='密码')
    phone = db.Column(db.String(50))
    id_card = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)
    hire_date = db.Column(db.DateTime)
    resign_date = db.Column(db.DateTime)
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    DESCRIPTION = db.Column(db.String(200))
    ISACTIVE = db.Column(db.String(10))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    REMOVE = db.Column(db.String(1))
