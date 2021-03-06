import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import socket
import struct
import numpy as np

host = '192.168.30.37'   ###address of the server
port = 9092

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host , port))

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    img = frame.array  
    img_crp = img[250:640,150:490]  #crop image lower half
    
       
        
    frame = cv2.cvtColor(img_crp, cv2.COLOR_BGR2GRAY)
   
    d = frame.flatten ()
    s = d.tostring ()
    print len(s)
    ft = time.time()
    sock.send(s)
    time.sleep(0.1)
    
    dat = sock.recvfrom(1024)
       
    tim = time.time()-ft
    print "time took  :",tim   
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    rawCapture.truncate(0)
    time.sleep(0.01)
camera.release()
cv2.destroyAllWindows() 
