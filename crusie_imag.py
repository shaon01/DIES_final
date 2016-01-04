import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')


from picamera.array import PiRGBArray
from picamera import PiCamera

from oct2py import octave
octave.addpath('./for_octave/image_matlab')
import time
import cv2

import struct, time
from RobotCommunication import SerialCommands

robot = SerialCommands('/dev/ttyAMA0',115200)
print robot.init()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

cruise_distance = 200 ## in mm
v_max = 155 ## in mm/s
v_curr = 1
a_max = 10

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
def findDist():
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array               #take image
    
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert to grayscale image
    
    cv2.imwrite('cam.jpg',frame)   #save image
    time.sleep(0.5)                #wait to save the image
    imt = cv2.imread('cam.jpg')    #read the saved image

    print 'send image'
    x = octave.getDistance(imt)   #call matlab with the saved image and get the distance.  x == 100 or 50 means there is no spirals
    
    return x*10
    
def cruiseControl(cam_distance):
    
    global v_curr   
    brk_dist =  cam_distance
    ctr_dist = ((0.5*v_curr*v_curr)/a_max )+cruise_distance
    print"------------------"
    print "brk_dist :",brk_dist
    print "ctr_dist :",ctr_dist
    print"------------------"
        
    
    if (ctr_dist < brk_dist):
        v_curr = min(v_max, v_curr+a_max)
        robot.startLineFollowing(int(v_curr*0.645))
        print "safe v_curr",v_curr*0.645
        
    else:
        v_curr = max(2, v_curr - a_max)
        robot.startLineFollowing(int(v_curr*0.645))
        print "critical v_curr",v_curr*0.645
            

    
if __name__ == '__main__':
    
    max_time = 30
    start_time = time.time()  # remember when we started
    while (time.time() - start_time) < max_time:
    
        x = findDist()
        cruiseControl(x)
        print x
    robot.init()
    
    
