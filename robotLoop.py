from ServerCom import ServerCom
import lcm
from robotlcm import robotFeedback_t, robotSettings_t
import thread
import time

serverCom = ServerCom() # Data used by robot
#serverCom.displayData() # Test


def my_handler(channel, data):
   print "received " + channel
   if channel in "ServerToRobot":
      global serverCom
      msg = robotSettings_t.decode(data)
      serverCom.setDesiredSpeed = msg.desiredSpeed
      serverCom.longitude = msg.positionFromGPS[0]
      serverCom.latitude = msg.positionFromGPS[1]
      serverCom.jawRate = msg.positionFromGPS[2]
      serverCom.setChangeLane = msg.changeLane

def receiveFromServer(freq):
   lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")
   subscription = lc.subscribe("ServerToRobot", my_handler)
   try:
      while 1:
	 time.sleep(1.0/freq)
         lc.handle()
   except KeyboardInterrupt:
      pass

# Define a function for the thread
def comServerThread(serverCom, freq):
   while True:
      time.sleep(1.0/freq)
      print "send"
      serverCom.sendToServer()

# Create two threads as follows
freqReceive = 10 #receiving
freqSend = 10 #sending
try:
   thread.start_new_thread( comServerThread, (serverCom, freqReceive, ) )
   thread.start_new_thread( receiveFromServer, (freqSend, ) )
except:
   print "Error: unable to start thread"

while 1:
   #print "test"
   time.sleep(0.01)
   #lc = lcm.LCM()
   #subscription = lc.subscribe("RobotToServer", my_handler)
   #try:
   #   while True:
   #      lc.handle()
   #except KeyboardInterrupt:
   #   pass
