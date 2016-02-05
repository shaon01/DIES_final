import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from picamera.array import PiRGBArray
from picamera import PiCamera

import time
import cv2
import numpy as np
from RobotCommunication import SerialCommands

import socket
import scipy.integrate

cruise_dist =300
v_desr = 100

host = '192.168.30.37'   ###address of the server
port = 9092

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host , port))

robot = SerialCommands('/dev/ttyAMA0',115200)
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
    

    
if __name__ == '__main__':
    
    robot.startLineFollowing(50)
    v_now = 60
    dist,t_im= findDist()
    P = 18
    I = 1
    err = 0
    while (1):
                
        if dist>0:
			
                if dist >= cruise_dist:
                    err_prev = err
                    err = (dist-v_now*t_im) - cruise_dist
                    i_err = scipy.integrate.simps([int(err_prev), int(err)])
                    err_new = P*err + I*i_err
                    temp_sp  =  min(v_desr, err*t_im)
                    v_now = max(temp_sp,0)
                    robot.startLineFollowing(int(v_now*0.645))
                    dist,t_im= findDist()
                    
                    
                else:
                    v_now = 0
                    robot.startLineFollowing(0)
                    dist,t_im= findDist()
                
            
                print 'in if:',v_now
                
                
        else:
            v_now = v_desr
            robot.startLineFollowing(int (v_now*0.645))
            dist,t_im = findDist()
            
            print 'in else'
                                 
        #~ print 'distance :',real_dist
        print 'current speed :',v_now
        print '-------------------------------'
        time.sleep(0.01)
        
    print robot.init()
    
    
