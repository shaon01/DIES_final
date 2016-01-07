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
    time.sleep(0.1)                #wait to save the image
    imt = cv2.imread('cam.jpg')    #read the saved image

    #print 'send image'
    ft = time.time()
    x = octave.findDistance(imt)   #call matlab with the saved image and get the distance.  x == 2 means there is no spirals
    tim = time.time()-ft
    print "time took  :",tim
    
    rawCapture.truncate(0)
    
    return x*10,tim     #return distance in mm
    

            

    
if __name__ == '__main__':
    
    max_time = 620
    start_time = time.time()  # remember when we started
    dist,t_im= findDist()
    
    while (time.time() - start_time) < max_time:
        dist,t_im= findDist()  
        if dist == 20:
            while dist == 20:
                
                v_now = robot.cruiseControl(2000) #no spirals so increase speed
                dist,t_im= findDist()
                
                print 'first loop dist :',dist
                print 'v_now :',v_now
            
        else:
            real_dist = dist - (v_now*t_im)
            while v_now > 2:
                v_now = robot.cruiseControl(real_dist) #no spirals so increase speed
                dist,t_im= findDist()
                if dist == 20:
                    real_dist = real_dist - (v_now*t_im)
                    
                else:
                    real_dist = dist - (v_now*t_im)
                    
                print 'second loop real distance :',real_dist
                print 'got  distance :',dist
                print 'v_now :',v_now
                        
        print "----------------------"
        time.sleep(0.02)
    robot.init()
    
    
