from GPSServerConnection import GPSServerConnection
from RobotCommunication import SerialCommands
import numpy as np

import time

gps_pos = GPSServerConnection()
robot = SerialCommands('/dev/ttyAMA0',115200)

pos_x=[]
pos_y=[]

if __name__ == '__main__':
		
	pos,t = gps_pos.getPosition(1)
	pos_x.append(pos[0])
	pos_y.append(pos[1])
	
	robot.startLineFollowing(20)

	
	for i in range(1,40):
		
		pos_x.append(pos_x[i-1]+ (20*0.465*0.2)*0.2516)
		pos_y.append(pos_y[i-1])

		
		time.sleep(0.2)
		
	print pos_x[39]
	
	robot.init()
	print gps_pos.getPosition(1)
		
			

