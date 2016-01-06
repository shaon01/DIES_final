import struct, time
from RobotCommunication import SerialCommands

robot = SerialCommands('/dev/ttyAMA0',115200)
print robot.init()


if __name__ == '__main__':

	cam_distance = 500
	
	for i in range(1,800):
		
		if i>300 and i<500:
			cam_distance = 700 - i
			
		else:
			cam_distance =500
		
		print ("*************************")
		print "cam_distance : ",cam_distance
		
		print ("*************************")
		print robot.cruiseControl(cam_distance)
		
		time.sleep(0.3)
	
robot.init()

		
		
	
