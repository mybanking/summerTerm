# coding=utf-8
from app import db


class VolunteerInfo(db.Model):
    __tablename__ = 'volunteer_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ORG_ID = db.Column(db.Integer)
    CLIENT_ID = db.Column(db.Integer)
    name = db.Column(db.String(50), info='姓名')
    gender = db.Column(db.String(5), info='性别')
    phone = db.Column(db.String(50))
    id_card = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)
    checkin_date = db.Column(db.DateTime)
    checkout_date = db.Column(db.DateTime)
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    DESCRIPTION = db.Column(db.String(200))
    ISACTIVE = db.Column(db.String(10))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    REMOVE = db.Column(db.String(1))
