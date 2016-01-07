import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from picamera.array import PiRGBArray
from picamera import PiCamera

import time
import cv2

from RobotCommunication import SerialCommands

import socket

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
    
    img_crp = img[250:640,0:640]  #crop image lower half
    frame = cv2.cvtColor(img_crp, cv2.COLOR_BGR2GRAY)
   
    d = frame.flatten ()
    s = d.tostring ()
  
    ft = time.time()
    sock.send(s)
    time.sleep(0.01)
    
    temp_data = sock.recvfrom(1024)
    dist = ord(temp_data[0])
    
   
    tim = time.time()-ft
    print "time took  :",tim  
    
    rawCapture.truncate(0)
    
    return dist*10,tim     #return distance in mm
    

    
if __name__ == '__main__':
    
    max_time = 240
    start_time = time.time()  # remember when we started
    
    v_now = robot.cruiseControl(2000)
    
    while (time.time() - start_time) < max_time:
        
        dist,t_im= findDist()
        real_dist = dist - (v_now*t_im)
        v_now = robot.cruiseControl(dist)
        print 'distance :',real_dist
        print 'current speed :',v_now
        print '-------------------------------'
        time.sleep(0.01)
        
    print robot.init()
    
    
