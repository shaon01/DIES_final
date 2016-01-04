
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from picamera.array import PiRGBArray
from picamera import PiCamera

from oct2py import octave
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
#camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    img = frame.array                #take image
    
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #convert to grayscale image
    
    cv2.imwrite('cam.jpg',frame)   #save image
    time.sleep(0.5)                #wait to save the image
    imt = cv2.imread('cam.jpg')    #read the saved image

    print 'send image'
    x = octave.getDistance(imt)   #call matlab with the saved image and get the distance.  x == 100 or 50 means there is no spirals
    print x
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    rawCapture.truncate(0)

camera.release()
cv2.destroyAllWindows() 
