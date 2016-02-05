#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ServerCom import ServerCom
import lcm
from robotlcm import robotFeedback_t, robotSettings_t
import thread
import time
from RobotCommunication import *


import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import numpy as np

import socket
import scipy.integrate

robot = SerialCommands('/dev/ttyAMA0',115200)

serverCom = ServerCom() # Data used by robot
#serverCom.displayData() # Test


cruise_dist =300
v_desr = 100

host = '192.168.30.37'   ###address of the server
port = 9092

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host , port))

print robot.init()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)



def findDist():
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array               #take image
    
    img_crp = img[250:640,150:490]  #crop image lower half
    frame = cv2.cvtColor(img_crp, cv2.COLOR_BGR2GRAY)
   
    d = frame.flatten ()
    s = d.tostring ()
  
    ft = time.time()
    sock.send(s)
    
    
    temp_data = sock.recvfrom(1024)
    dist = ord(temp_data[0])
    
   
    tim = time.time()-ft
    print "time took  :",tim  
    
    rawCapture.truncate(0)
    
    return dist*10,tim     #return distance in mm


def my_handler(channel, data):
   if channel in "ServerToRobot":
      #print "receive"
      global serverCom
      msg = robotSettings_t.decode(data)
      serverCom.desiredSpeed = msg.desiredSpeed
      serverCom.longitude = msg.positionFromGPS[0]
      serverCom.latitude = msg.positionFromGPS[1]
      serverCom.jawRate = msg.positionFromGPS[2]
      serverCom.changeLane = msg.changeLane

def receiveFromServer(freq):
   lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")
   subscription = lc.subscribe("ServerToRobot", my_handler)
   try:
      while 1:
         lc.handle()
         time.sleep(1.0/freq)
   except KeyboardInterrupt:
      pass

# Define a function for the thread
def comServerThread(serverCom, freq):
   while True:
      time.sleep(1.0/freq)
      serverCom.sendToServer()
      
      

# Create two threads as follows
freqReceive = 10 #receiving
freqSend = 10 #sending
try:
   thread.start_new_thread( comServerThread, (serverCom, freqReceive, ) )
   thread.start_new_thread( receiveFromServer, (freqSend, ) )
except:
   print "Error: unable to start thread"

oldDesired = serverCom.desiredSpeed
#robot.startLineFollowing(serverCom.desiredSpeed)
print serverCom.desiredSpeed
print "--- Robot start"
robot.startLineFollowing(int(serverCom.desiredSpeed))
v_now = 0
dist,t_im= findDist()
P = 18
I = 1
err = 0
while 1:
   serverCom.currentSpeed = v_now
#   serverCom.displayData()
   if dist>0:
        
        if dist >= cruise_dist:
            err_prev = err
            err = (dist-v_now*t_im) - cruise_dist
            i_err = scipy.integrate.simps([int(err_prev), int(err)])
            err_new = P*err + I*i_err
            temp_sp  =  min(int(serverCom.desiredSpeed), err*t_im)
            v_now = max(temp_sp,0)
            if dist<400:
               v_now = 0
            robot.startLineFollowing(int(v_now*0.645))
            dist,t_im= findDist()
            
            
        else:
            v_now = 0
            robot.startLineFollowing(0)
            dist,t_im= findDist()
        
    
 #       print 'in if:',v_now
          
            
   else:
        v_now = int(serverCom.desiredSpeed)
        robot.startLineFollowing(int (v_now*0.645))
        dist,t_im = findDist()
   serverCom.currentSpeed = v_now
   if(serverCom.changeLane):
      if(serverCom.currentLane == 0):
         robot.laneChange(-1, serverCom.desiredSpeed)
         serverCom.currentLane = 1
      else:
         robot.laneChange(1, serverCom.desiredSpeed)
         serverCom.currentLane = 0
      serverCom.changeLane = False
       # print 'in else'
                             
    #~ print 'distance :',real_dist
#   print 'current speed :',v_now
#   print '-------------------------------'
   time.sleep(0.01)
    
print robot.init()
   
   
   
