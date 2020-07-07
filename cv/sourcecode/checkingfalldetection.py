# -*- coding: utf-8 -*-
'''
摔倒检测模型主程序

用法：
python checkingfalldetection.py
python checkingfalldetection.py --filename ../images/tests/videos/3.mp4
'''

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2
import os
import time
import subprocess
import argparse
from oldcare.api import SmileApi
import math 
import threading
import imutils


img=''
a=''
f=""


class Checkingfalldetection():

    
    def __init__(self,filename):
        self.filename= filename
        
            #线程处理
    def run1(self):
          
            biaoqing = SmileApi()
            while True:
                global a
                global img
                if img!='':
                    a = biaoqing.detect_fall(img)

    #连接骨架函数
    def connect_skeleton(self,image,skeleton1,skeleton2,left,top,color):
        cv2.line(image, (int(skeleton1.get('x'))+int(left),int(skeleton1.get('y'))+int(top)), (int(skeleton2.get('x'))+int(left),int(skeleton2.get('y'))+int(top)), color, 2)
            #计算角度
    def calc_angle(self,x1, y1, x2, y2):

        x = abs(x1 - x2)

        y = abs(y1 - y2)

        z = math.sqrt(x * x + y * y)

        angle = round(math.asin(y / z) / math.pi * 180)

        return angle

    def run(self):
        global a
        global img

        # threadmax = threading.BoundedSemaphore(20)
        # 传入参数
        # ap = argparse.ArgumentParser()
        # ap.add_argument("-f", "--filename", required=False, default = '',
        #     help="")
        # args = vars(ap.parse_args())
        input_video = "../images/tests/videos/3.mp4"
        
        # 控制陌生人检测
        fall_timing = 0 # 计时开始
        fall_start_time = 0 # 开始时间
        fall_limit_time = 1 # if >= 1 seconds, then he/she falls.

        output_fall_path = '../supervision/fall'
        # your python path
        python_path = '/home/kdy/anaconda3/envs/tensorflow/bin/python'

        # model_path = '../models/fall_detection.hdf5'
        # # 加载模型
        # model = load_model(model_path)
        # 全局常量
        TARGET_WIDTH = 64
        TARGET_HEIGHT = 64

        # 初始化摄像头
        if not input_video:
            vs = cv2.VideoCapture(0)
            time.sleep(2)
        else:
            vs = cv2.VideoCapture(input_video)
            print("开始骨骼检测")
            # vs = cv2.VideoCapture(0)
        #
        a={"skeletons":[]}
        #开启线程
        t1 = threading.Thread(target=self.run1) 
        t1.start()
                    
        print('[INFO] 开始检测是否有人摔倒...')
        # 不断循环
        counter = 0
        while True:
            
            counter += 1
            # grab the current frame
            (grabbed, image) = vs.read()

            # if we are viewing a video and we did not grab a frame, then we
            # have reached the end of the video
            if input_video and not grabbed:
                break
            
            if not input_video:
                image = cv2.flip(image, 1)


            roi= cv2.resize(image, (TARGET_WIDTH, TARGET_HEIGHT))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            img = cv2.imencode(".jpg", image)[1].tobytes()
            
            # # cv2.imwrite(os.path.join("./supervision","temp.jpg"),image) 
            if a.get("skeletons"):
                # print(a)
                    
                for b in a.get("skeletons"):
                    landmark=b.get("landmark")
                    left=b.get("body_rectangle").get("left")
                    top=b.get("body_rectangle").get("top")
                    width=b.get("body_rectangle").get("width")
                    height=b.get("body_rectangle").get("height")
                    # print(b)
                    cv2.rectangle(image, (int(left), int(top)), (int(left)+int(width), int(top)+int(height)), (0, 0, 255), 2)
                    head=landmark.get("head")
                    neck=landmark.get("neck")
                    left_shoulder=landmark.get("left_shoulder")
                    right_shoulder=landmark.get("right_shoulder")
                    left_hand=landmark.get("left_hand")
                    right_hand=landmark.get("right_hand")
                    left_buttocks=landmark.get("left_buttocks")
                    right_buttocks=landmark.get("right_buttocks")
                    left_knee=landmark.get("left_knee")
                    right_knee=landmark.get("right_knee")
                    left_foot=landmark.get("left_foot")
                    right_foot=landmark.get("right_foot")

                    self.connect_skeleton(image,head,neck,left,top,(0,255,0))
                    self.connect_skeleton(image,neck,left_shoulder,left,top,(0,255,0))
                    self.connect_skeleton(image,neck,right_shoulder,left,top,(0,255,0))
                    self.connect_skeleton(image,right_hand,right_shoulder,left,top,(255,20,147))
                    self.connect_skeleton(image,left_hand,left_shoulder,left,top,(255,20,147))
                    self.connect_skeleton(image,neck,left_buttocks,left,top,(0,255,0))
                    self.connect_skeleton(image,neck,right_buttocks,left,top,(0,255,0))
                    self.connect_skeleton(image,right_buttocks,right_knee,left,top,(255,255,0))
                    self.connect_skeleton(image,left_buttocks,left_knee,left,top,(255,255,0))
                    self.connect_skeleton(image,left_knee,left_foot,left,top,(255,255,0))
                    self.connect_skeleton(image,right_knee, right_foot,left,top,(255,255,0))   

                
            # cv2.imshow("123",image)
            # time.sleep(100)
            # exit()
            # determine facial expression

            
            if a.get("skeletons"):
                
                for b in a.get("skeletons"):
                        landmark=b.get("landmark")
                        width=b.get("body_rectangle").get("width")
                        height=b.get("body_rectangle").get("height")
                        head=landmark.get("head")
                        left_buttocks=landmark.get("left_buttocks")
                        right_buttocks=landmark.get("right_buttocks")
                        mid_buttocks_x=int(left_buttocks.get('x'))+int(right_buttocks.get('x'))
                        mid_buttocks_x=mid_buttocks_x/2
                        mid_buttocks_y=int(left_buttocks.get('y'))+int(right_buttocks.get('y'))
                        mid_buttocks_y=mid_buttocks_y/2
                        
                        right_foot=landmark.get("right_foot")
                        left_foot=landmark.get("left_foot")
                        mid_foot_x=int(right_foot.get('x'))+int(left_foot.get('x'))
                        mid_foot_x=mid_foot_x/2
                        mid_foot_y=int(right_foot.get('y'))+int(left_foot.get('y'))
                        mid_foot_y=mid_foot_y/2

                        # if width>height:
                        #     index=1
                        #     break
                        # print('zzz')
                        print(self.calc_angle(mid_buttocks_x,mid_buttocks_y,int(head.get('x')),int(head.get('y'))))
                        print(self.calc_angle(mid_foot_x,mid_foot_y,mid_buttocks_x,mid_buttocks_y))
                        if abs(self.calc_angle(mid_buttocks_x,mid_buttocks_y,int(head.get('x')),int(head.get('y'))))<60 and abs(self.calc_angle(mid_foot_x,mid_foot_y,mid_buttocks_x,mid_buttocks_y))<60:
                            index=1
                            break
                        else:
                            index=0


                if index==1:
                    fall=self.calc_angle(mid_buttocks_x,mid_buttocks_y,int(head.get('x')),int(head.get('y')))
                    normal=0
                else:
                    fall=0
                    normal=self.calc_angle(mid_buttocks_x,mid_buttocks_y,int(head.get('x')),int(head.get('y')))

            else:
                # (fall, normal) = model.predict(roi)[0]
                fall=0
                normal=1
                    
                
                
            # display the label and bounding box rectangle on the output frame
            label = "Fall (%.2f)" %(fall) if fall > normal else "Normal (%.2f)" %(normal)
            cv2.putText(image, label, (image.shape[1] - 150, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            
            if fall > normal:
                if fall_timing == 0: # just start timing
                    fall_timing = 1
                    fall_start_time = time.time()
                else: # alredy started timing
                    fall_end_time = time.time()
                    difference = fall_end_time - fall_start_time
                        
                    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                time.localtime(time.time()))
                    
                    if difference < fall_limit_time:
                        print('[INFO] %s, 走廊, 摔倒仅出现 %.1f 秒. 忽略.' %(current_time, difference))
                    else: # strangers appear
                        event_desc = '有人摔倒!!!'
                        event_location = '走廊'
                        print('[EVENT] %s, 走廊, 有人摔倒!!!' %(current_time))
                        cv2.imwrite(os.path.join(output_fall_path, 
                                                'snapshot_%s.jpg' %(time.strftime('%Y%m%d_%H%M%S'))), image)# snapshot
                        # insert into database
                        command = '%s inserting.py --event_desc %s --event_type 3 --event_location %s' %(python_path, event_desc, event_location)
                        p = subprocess.Popen(command, shell=True)  

            global f
            f=image
            # print("new")
            cv2.imshow('Fall detection', image)

                
                
            
            # Press 'ESC' for exiting video
            k = cv2.waitKey(1) & 0xff 
            if k == 27:
                break



        vs.release()
        cv2.destroyAllWindows()
    def startfall(self):
        #开启线程
        t = threading.Thread(target=self.run) 
        t.start()
    def get_frame(self):
        global f
        if f!="":
            ret, jpeg = cv2.imencode('.jpg', f)
            # ret, jpeg = cv2.imencode('.jpg', )
            return jpeg.tobytes()
        else:
            return None