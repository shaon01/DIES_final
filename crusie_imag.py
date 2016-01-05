import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')


from picamera.array import PiRGBArray
from picamera import PiCamera

from oct2py import octave
#octave.addpath('./for_octave/image_matlab')
import time
import cv2

import struct, time
from RobotCommunication import SerialCommands

robot = SerialCommands('/dev/ttyAMA0',115200)
print robot.init()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))

cruise_distance = 200 ## in mm
v_max = 80 ## in mm/s
v_curr = 1
a_max = 2

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
def findDist():
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array               #take image
    
    imgc = img[250:640,0:640]  #crop image lower half
    
    cv2.imshow("image",imgc)
    cv2.waitKey(1)
    
    cv2.imwrite('cam.jpg',imgc)    #save image
    time.sleep(0.5)                #wait to save the image
    imt = cv2.imread('cam.jpg')    #read the saved image

    #print 'send image'
    ft = time.time()
    x = octave.findDistance(imt)   #call matlab with the saved image and get the distance.  x == 100 or 50 means there is no spirals
    tim = time.time()-ft
    print "time took  :",tim
    
    rawCapture.truncate(0)
    
    return x*10
    
def cruiseControl(cam_distance):
    
    global v_curr   
    brk_dist =  cam_distance
    ctr_dist = ((0.5*v_curr*v_curr)/a_max )+cruise_distance
    '''
    print"------------------"
    print "brk_dist :",brk_dist
    print "ctr_dist :",ctr_dist
    print"------------------"
    '''    
    
    if (ctr_dist < brk_dist):
        v_curr = min(v_max, v_curr+a_max)
        robot.startLineFollowing(int(v_curr*0.645))
        print "safe v_curr",v_curr*0.645
        
    else:
        v_curr = max(2, v_curr - a_max)
        robot.startLineFollowing(int(v_curr*0.645))
        print "critical v_curr",v_curr*0.645
            

    
if __name__ == '__main__':
    
    max_time = 60
    start_time = time.time()  # remember when we started
    while (time.time() - start_time) < max_time:
    
        x = findDist()
        #cruiseControl(x)
        print 'current distance :',x
        print "----------------------"
        time.sleep(0.2)
    robot.init()
    
    
