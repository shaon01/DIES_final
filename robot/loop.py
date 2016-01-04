#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ServerCom import ServerCom
import lcm
from robotlcm import robotFeedback_t, robotSettings_t
import thread
import time
from RobotCommunication import *

robot = SerialCommands('/dev/ttyAMA0',115200)

serverCom = ServerCom() # Data used by robot
#serverCom.displayData() # Test


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
while 1:
  #print serverCom.desiredSpeed
   if oldDesired != serverCom.desiredSpeed:
      robot.startLineFollowing(serverCom.desiredSpeed) ###start line following with speed 1-127
      oldDesired = serverCom.desiredSpeed
   if(serverCom.changeLane):
      if(serverCom.currentLane == 0):
         robot.laneChange(-1, serverCom.desiredSpeed)
         serverCom.currentLane = 1
      else:
         robot.laneChange(1, serverCom.desiredSpeed)
         serverCom.currentLane = 0
      serverCom.changeLane = False
      oldDesired = -1
      
   time.sleep(1)
   
