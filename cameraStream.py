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

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((host , port))

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
    img_crp = img[250:640,0:640]  #crop image lower half
    
    for_red = img_crp
    img_hsv=cv2.cvtColor(for_red, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
    
    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
    
    # join my masks
    mask = mask0+mask1
    
    # set my output img to zero everywhere except my mask
    output_img = img_crp.copy()
    output_img[np.where(mask==0)] = 0
    cv2.imshow('far',output_img)
    '''    
    frame = cv2.cvtColor(img_crp, cv2.COLOR_BGR2GRAY)
   
    d = frame.flatten ()
    s = d.tostring ()
    ft = time.time()
    sock.send(s)
    time.sleep(0.1)
    
    dat = sock.recvfrom(1024)
       
    tim = time.time()-ft
    print "time took  :",tim   
    '''
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    rawCapture.truncate(0)
    time.sleep(0.01)
camera.release()
cv2.destroyAllWindows() 
