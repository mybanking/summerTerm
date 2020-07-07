# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
import json
import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(0,640) # set Width (the first parameter is property_id)
cap.set(1,480) # set Height
time.sleep(2)


for i in range(10):# 拍100张图片就结束
    ret, img = cap.read()
    cv2.imshow('img', img)
    cv2.imwrite('image/%d.jpg' %(i), img)
    
	# Press 'ESC' for exiting video
    k = cv2.waitKey(100) & 0xff 
    if k == 27:
        break
 
cap.release()
cv2.destroyAllWindows()

http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
key = "VfFq28mDLp1hLWXKGXVfNGO8LUKvpTBs"
secret = "m1GTqEqGungSNT-J6YIn4MobFsAEOpkL"
filepath = r"/home/sara/Desktop/test/image/9.jpg"

boundary = '----------%s' % hex(int(time.time() * 1000))
data = []
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
data.append(key)
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
data.append(secret)
data.append('--%s' % boundary)
fr = open(filepath, 'rb')
data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
data.append('Content-Type: %s\r\n' % 'application/octet-stream')
data.append(fr.read())
fr.close()
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
data.append('1')
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
data.append(
    "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
data.append('--%s--\r\n' % boundary)

for i, d in enumerate(data):
    if isinstance(d, str):
        data[i] = d.encode('utf-8')

http_body = b'\r\n'.join(data)

# build http request
req = urllib.request.Request(url=http_url, data=http_body)

# header
req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

try:
    # post data to server
    resp = urllib.request.urlopen(req, timeout=5)
    # get response
    qrcont = resp.read()
    # if you want to load as json, you should decode first,
    rsp = json.loads(qrcont.decode('utf-8'))
    # print(qrcont.decode('utf-8'))
    # print(rsp)
    # print(type(rsp))
    print(rsp['faces'][0]['attributes']['glass']['value'])
    if rsp['faces'][0]['attributes']['glass']['value']=='Normal':
     print("please take off your glasses")
    elif rsp['faces'][0]['attributes']['glass']['value']=='Dark':
     print("please take off your dark glasses")
except urllib.error.HTTPError as e:
    print(e.read().decode('utf-8'))
