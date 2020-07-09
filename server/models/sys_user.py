# coding=utf-8
from app import db


class SysUser(db.Model):
    __tablename__ = 'sys_user'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ORG_ID = db.Column(db.Integer, nullable=False)
    CLIENT_ID = db.Column(db.Integer, nullable=False)
    UserName = db.Column(db.String(50), nullable=False, info='用户名')
    Password = db.Column(db.String(50), info='密码')
    REAL_NAME = db.Column(db.String(50))
    SEX = db.Column(db.String(20))
    EMAIL = db.Column(db.String(50))
    PHONE = db.Column(db.String(50))
    MOBILE = db.Column(db.String(50))
    DESCRIPTION = db.Column(db.String(200))
    ISACTIVE = db.Column(db.String(10))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    REMOVE = db.Column(db.String(1))
    DATAFILTER = db.Column(db.String(200))
    theme = db.Column(db.String(45))
    defaultpage = db.Column(db.String(45), info='登录成功页面')
    logoimage = db.Column(db.String(45), info='显示不同logo')
    qqopenid = db.Column(db.String(100), info='第三方登录的凭证')
    appversion = db.Column(db.String(10), info='检测app的版本号')
    jsonauth = db.Column(db.String(1000), info=' app权限控制')

