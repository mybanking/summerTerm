# coding=utf-8
from app import db


class EventInfo(db.Model):
    __tablename__ = 'event_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_type = db.Column(db.Integer, info='事件类型')
    event_date = db.Column(db.DateTime)
    event_location = db.Column(db.String(200))
    event_desc = db.Column(db.String(200))
    oldperson_id = db.Column(db.ForeignKey('oldPerson_info.ID'), index=True)

    oldperson = db.relationship('OldPersonInfo', primaryjoin='EventInfo.oldperson_id == OldPersonInfo.ID',
                                backref='event_infos')