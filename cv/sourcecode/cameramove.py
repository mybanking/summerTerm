# -*- coding: utf-8 -*-
'''
实现自动运镜以解决镜头不能自主移动的问题
参数依次为该帧对象、画面宽度、高度，跟踪框上端坐标下端坐标，左端和右端坐标
'''

# 导入包
import imutils

def cameramove(frame,width,height,top,bottom,left,right):
    the_width = 0.8*width
    the_height = 0.8*height
    t = (top+bottom)/2-the_height/2
    b = (top+bottom)/2+the_height/2
    l = (left+right)/2-the_width/2
    r = (left+right)/2+the_width/2
    if t<0:
        t = 0
    if b>the_height:
        b = the_height
    if l<0:
        l = 0
    if r > the_width:
        r = the_width
    #frame = frame[int(top*0.85):int(bottom*1.06),int(left*0.85):int(right*1.06)]
    frame = frame[int(t):int(b),int(l):int(r)]
    frame = imutils.resize(frame, width = width, height = height)#压缩，加快识别速度
    return frame
