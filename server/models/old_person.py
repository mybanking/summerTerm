# coding=utf-8
from app import db


class OldPersonInfo(db.Model):
    __tablename__ = 'oldPerson_info'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ORG_ID = db.Column(db.Integer, info='没用到')
    CLIENT_ID = db.Column(db.Integer, info='没用到')
    username = db.Column(db.String(50), info='用户名')
    gender = db.Column(db.String(5), info='性别')
    phone = db.Column(db.String(50))
    id_card = db.Column(db.String(50))
    birthday = db.Column(db.DateTime)
    checkin_date = db.Column(db.DateTime)
    checkout_date = db.Column(db.DateTime)
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    room_number = db.Column(db.String(50))
    firstguardian_name = db.Column(db.String(50))
    firstguardian_relationship = db.Column(db.String(50))
    firstguardian_phone = db.Column(db.String(50))
    firstguardian_wechat = db.Column(db.String(50))
    secondguardian_name = db.Column(db.String(50))
    secondguardian_relationship = db.Column(db.String(50))
    secondguardian_phone = db.Column(db.String(50))
    secondguardian_wechat = db.Column(db.String(50))
    health_state = db.Column(db.String(50))
    DESCRIPTION = db.Column(db.String(200))
    ISACTIVE = db.Column(db.String(10))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    REMOVE = db.Column(db.String(1))

    def __repr__(self):
        return {
            'id': self.ID,
            'user Name': self.username,
            'gender': self.gender
        }

    def to_json(self):
        return {
            'id': self.ID,
            'user Name': self.username,
            'gender': self.gender
        }
