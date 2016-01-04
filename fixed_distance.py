
#!/usr/bin/env python
# -*- coding: utf-8 


import struct, time
from RobotCommunication import SerialCommands

robot = SerialCommands('/dev/ttyAMA0',115200)
print robot.init()

def fixedDistance(dist_to_go):

	data = robot.readEncoders()
	dist = 0
	
	while (len(data)!=8):
		data = robot.readEncoders()
		time.sleep(0.1)
				
	old = struct.unpack('<ii',data)
	data = 0
		
	robot.startLineFollowing(100)
	
	while(dist <= dist_to_go):
		
		data = robot.readEncoders()
		time.sleep(0.1)
		while (len(data)!=8):  
			time.sleep(0.1)			###reading encoders
			data = robot.readEncoders()
			
			
				
		new = struct.unpack('<ii',data)
		data = 0
			
			
		dist = (((new[1]- old[1]) + (new[0] - old[0]))/2)*0.1627   # take the average of encoders and multipy by 1 tick = 0.1627mm
		print dist
	
	robot.init()


if __name__ == '__main__':
	robot.fixedDistance(1000)

	



		


