# coding=utf-8
import json
import time
import base64

from flask import Flask, render_template, Response, request, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *

# from VideoCamera.camera import VideoCamera
from response import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
# 连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://djd:dongjinda@cdb-3stfljwg.cd.tencentcdb.com:10031/OldCare'
# 每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

# session 秘钥
app.config['SECRET_KEY'] = 'oldCare'

db = SQLAlchemy(app)
db.create_all()

from models.models import *


# select old person
@app.route('/getOldPersonInfo', methods=['GET'])
def get_old_person_info():
    result_list = []
    for result in OldPersonInfo.query.all():
        result_list.append(result.to_json())

    response = DataResponse(code=0, data=result_list, msg='Succeed to select all old persons!')
    response = json.dumps(response.__dict__)

    return response


# insert old person
@app.route('/addOldPersonInfo', methods=['POST'])
def add_old_person_info():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    old_person = OldPersonInfo(username=body['username'], gender=body['gender'], CREATED=current_time)
    db.session.add(old_person)
    # db.session.commit()

    response = BaseResponse(code=0, msg='Succeed to insert one old person!')
    response = json.dumps(response.__dict__)

    return response


# delete old person
@app.route('/deleteOldPerson', methods=['POST'])
def delete_old_person():
    body = request.json
    old_person = OldPersonInfo(ID=body['id'], username=body['username'])
    db.session.delete(old_person)

    response = BaseResponse(code=0, msg="Succeed to delete one old person!")
    response = json.dumps(response.__dict__)

    return response


# update old person
@app.route('/updateOldPerson', methods=['POST'])
def update_old_person():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    OldPersonInfo.query.filter_by(ID=body['id']).update({'username': body['userName'], 'UPDATED': current_time})

    response = BaseResponse(code=0, msg="Succeed to update old person!")
    response = json.dumps(response.__dict__)

    return response


# insert volunteer
@app.route('/addVolunteer', methods=['POST'])
def add_volunteer():
    body = request.json
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    volunteer = VolunteerInfo(name=body['name'], gender=['gender'], CREATED=current_time)
    db.session.add(volunteer)

    response = BaseResponse(code=0, msg="Succeed to insert one volunteer!")
    response = json.dumps(response.__dict__)

    return response


# select events
# event_type = 0 => facial expression detection
#   anger, disgust, fear, happiness, neutral, sadness, surprise
# event_type = 1 => interaction detection
# event_type = 2 => stranger detection
# event_type = 3 => fall detection
# event_type = 4 => prohibit area intrusion detection
@app.route('/getFacialEvent', methods=['GET'])
def get_events():
    body = request.json
    result_list = []
    for result in EventInfo.query.filter_by(event_type=body['eventType']).all():
        result_list.append(result.to_json())

    response = DataResponse(code=0, data=result_list, msg='Succeed to get specific events!')
    response = json.dumps(response.__dict__)

    return response


# insert event
@app.route('/addEvent', methods=['POST'])
def add_event():
    body = request.json

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # stranger detection OR prohibit area intrusion detection
    if body['eventType'] == 2 or body['eventType'] == 4:
        event = EventInfo(event_type=body['eventType'], event_date=current_time, event_desc=body['eventDesc'])
    # facial expression detection OR interaction detection OR fall detection
    else:
        event = EventInfo(event_type=body['eventType'], event_date=current_time,
                          event_desc=body['eventDesc'], oldperson_id=body['oldPersonId'])
    db.session.add(event)

    response = BaseResponse(code=0, msg='Succeed to add event')
    response = json.dumps(response.__dict__)

    return response


# sys_user register
@app.route('/register', methods=['POST'])
def add_sys_usr():
    body = request.json
    sys_usr = SysUser(UserName=body['username'], Password=body['password'])
    db.session.add(sys_usr)

    response = BaseResponse(code=0, msg="Succeed to register")
    response = json.dumps(response.__dict__)

    return response


# sys_user login
@app.route('/login', methods=['POST'])
def login():
    body = request.json
    user_name = body['username']
    password = body['password']

    for result in SysUser.query.filter_by(UserName=user_name).all():
        if password == result.to_json()['password']:
            session['sys_user_id'] = result.to_json()['id']
            session['sys_user_name'] = result.to_json()['userName']
            response = BaseResponse(code=0, msg="Match")
            response = json.dumps(response.__dict__)
            return response
        else:
            continue
    response = BaseResponse(code=-1, msg="Not match")
    response = json.dumps(response.__dict__)
    return response


# index
@app.route('/index')
def index():
    # if 'sys_user_name' in session:
    #     sys_user_name = session['sys_user_name']

    # list of all result
    result_list = []

    # ======== 1st part ========

    # dict of first part
    result_dict_1 = {}

    # num of old person
    sql_1 = 'SELECT COUNT(oldPerson_info.username) FROM oldPerson_info'
    for result in db.session.execute(sql_1).first():
        result_dict_1['old_num'] = result

    # num of new old person today
    sql_2 = 'SELECT COUNT(oldPerson_info.username) FROM oldPerson_info WHERE TO_DAYS(CREATED) = TO_DAYS(NOW())'
    for result in db.session.execute(sql_2).first():
        result_dict_1['new_old_num'] = result

    # num of male and female old person
    sql_3 = 'SELECT gender, COUNT(username) FROM oldPerson_info GROUP BY gender'
    for result in db.session.execute(sql_3):
        result_dict_1[result[0]] = result[1]

    # num of volunteer
    sql_4 = 'SELECT COUNT(`name`) FROM volunteer_info'
    for result in db.session.execute(sql_4).first():
        result_dict_1['vol_num'] = result

    # num of new volunteer
    sql_5 = 'SELECT COUNT(`name`) FROM volunteer_info WHERE TO_DAYS(CREATED) = TO_DAYS(NOW())'
    for result in db.session.execute(sql_5).first():
        result_dict_1['new_vol_num'] = result

    result_list.append(result_dict_1)

    # ======== 2nd part ========

    # list of second part
    result_list_2 = []

    # num of all kinds of facial expression detection event
    sql_6 = "SELECT COUNT(id),	event_desc FROM	event_info WHERE event_type = 0 GROUP BY TO_DAYS(event_date) = TO_DAYS(NOW()), event_desc"
    for result in db.session.execute(sql_6):
        # dict of second part
        result_dict_2 = {'event_num': result[0], 'event_type': result[1]}
        result_list_2.append(result_dict_2)

    result_list.append(result_list_2)

    # ======== 3rd part ========

    # list of third part
    result_list_3_1 = []
    result_list_3_2 = []

    # dict of third part
    result_dict_3 = {}

    # fall and stranger in the past 10 days
    sql_7 = "SELECT COUNT(id),	event_desc, event_type, DATE_FORMAT(event_date,'%Y-%m-%d') FROM	event_info " \
            "WHERE (event_type = 3 OR event_type = 4) AND DATE_SUB(CURDATE(), INTERVAL 10 DAY) <= date(event_date) AND TO_DAYS(event_date) <= TO_DAYS(NOW()) " \
            "GROUP BY DATE_FORMAT(event_date,'%Y-%m-%d'), event_desc, event_type"

    for result in db.session.execute(sql_7):
        print(str(result))
        # fall
        if result[2] == 3:
            result_dict_3_1 = {"num": result[0], "even_desc": result[1], "event_date": result[3]}
            result_list_3_1.append(result_dict_3_1)
        # stranger
        elif result[2] == 4:
            result_dict_3_2 = {"num": result[0], "even_desc": result[1], "event_date": result[3]}
            result_list_3_2.append(result_dict_3_2)

    result_dict_3['fall_list'] = result_list_3_1
    result_dict_3['stranger'] = result_list_3_2

    result_list.append(result_dict_3)

    # ======== 4th part ========

    # list of fourth part
    result_list_4 = []

    # num of happiness
    sql_8 = "SELECT oldPerson_info.username, COUNT(event_info.id) FROM oldPerson_info, event_info " \
            "WHERE oldPerson_info.ID = event_info.oldperson_id AND event_info.event_type = 0 AND event_info.event_desc = 'happiness' " \
            "GROUP BY oldPerson_info.username ORDER BY COUNT(event_info.id) DESC LIMIT 5"
    rank = 1
    for result in db.session.execute(sql_8):
        result_dict_4 = {'rank': rank, 'user_name': result[0], 'happiness_count': result[1]}
        result_list_4.append(result_dict_4)
        rank += 1

    result_list.append(result_list_4)

    # ======== 5th part ========

    with open('picture/test.png', 'rb') as f:
        data = f.read()
        encode_str = str(base64.b64encode(data), 'utf-8')
        encode_str = "data:image/png;base64," + encode_str
        result_list.append({'pic_base64': encode_str})

    response = DataResponse(code=0, msg='Succeed to get info', data=result_list)
    response = json.dumps(response.__dict__)

    return response

    # return "Logged in as " + sys_user_name
    # else:
    #     response = BaseResponse(code=-1, msg='Please login')
    #     response = json.dumps(response.__dict__)
    #     return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
