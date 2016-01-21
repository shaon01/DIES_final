
#!/usr/bin/env python
# -*- coding: utf-8 


import struct, time
import kbhit
from RobotCommunication import SerialCommands

robot = SerialCommands('/dev/ttyAMA0',115200)
kb = kbhit.KBHit()

print robot.init()



if __name__ == '__main__':
	
	robot.startLineFollowing(20) ###start line following with speed 1-127
	
	
	while 1: 
		
		if kb.kbhit():  ### check if the key is pressed
			key = kb.getch()
			if key == 'r':   ##if pressed "r" go from left to right lane
				robot.laneChange(1)
			if key == 'l':   ##if pressed "l" go from right to left lane
				robot.laneChange(-1)
			if key == 's': ## if pressed "s" stop the robot
				robot.init()
				break
	
	
