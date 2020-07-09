# coding=utf-8
import json
import time

from flask import Flask, render_template, Response, request, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from VideoCamera.camera import VideoCamera
from response import *

app = Flask(__name__)
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
    old_person = OldPersonInfo(username=body['username'], gender=body['gender'])
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
    OldPersonInfo.query.filter_by(ID=body['id']).update({'username': body['userName']})

    response = BaseResponse(code=0, msg="Succeed to update old person!")
    response = json.dumps(response.__dict__)

    return response


# insert volunteer
@app.route('/addVolunteer', methods=['POST'])
def add_volunteer():
    body = request.json
    volunteer = VolunteerInfo(name=body['name'])
    db.session.add(volunteer)

    response = BaseResponse(code=0, msg="Succeed to insert one volunteer!")
    response = json.dumps(response.__dict__)

    return response


# select events
# event_type = 0 => facial expression detection
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


# 主页
@app.route('/')
def index():
    if 'sys_user_name' in session:
        sys_user_name = session['sys_user_name']
        return "Logged in as " + sys_user_name
    else:
        return "Please login"


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# 视频流传输
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
