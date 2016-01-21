import lcm
import time
from robotlcm import robotFeedback_t, robotSettings_t
import thread

lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")

class ServerCom:
   'Common base class for communication with server in robot project'  
   
   def __init__(self):
      self.longitude = 2.0
      self.latitude = 4.0
      self.jawRate = 5.0
      self.desiredSpeed = 0.0
      self.currentSpeed = 0.0
      self.currentLane = 0
      self.changeLane = False

   def sendToServer(self):
      global lc
      #self.displayData()
      msg = robotFeedback_t()
      msg.timestamp = int(time.time() * 1000000)
      msg.speedCurrent = self.currentSpeed;
      msg.positionEstimation = (self.longitude, self.latitude, self.jawRate)
      if self.currentLane == 0:
         msg.laneRight = True
      else:
         msg.laneRight = False
      lc.publish("RobotToServer", msg.encode())

   def displayData(self):
      print "| Longitude: ", self.longitude,  "\t, Latitude: ", self.latitude, "\t, Jaw Rate: ", self.jawRate 
      print "| Desired Speed: ", self.desiredSpeed, "\t, Current Speed: ", self.currentSpeed
      print "| Current Lane: ", self.currentLane, "\t, Change Lane?: ", self.changeLane

