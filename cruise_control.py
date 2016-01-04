import struct, time
from RobotCommunication import SerialCommands

robot = SerialCommands('/dev/ttyAMA0',115200)
print robot.init()


cam_distance = 500
cruise_distance = 200
v_max = 155 ##mm
v_curr = 1
a_max = 10
stop_cruise = False

def cruiseControl():
	
	global v_curr 	
	brk_dist =  cam_distance
	ctr_dist = ((0.5*v_curr*v_curr)/a_max )+cruise_distance
	print"------------------"
	print "brk_dist :",brk_dist
	print "ctr_dist :",ctr_dist
	print"------------------"
		
	
	if (ctr_dist < brk_dist):
		v_curr = min(v_max, v_curr+a_max)
		robot.startLineFollowing(int(v_curr*0.645))
		print "safe v_curr",v_curr*0.645
		
	else:
		v_curr = max(2, v_curr - a_max)
		robot.startLineFollowing(int(v_curr*0.645))
		print "critical v_curr",v_curr*0.645
			
			
			
if __name__ == '__main__':

	
	cruiseControl()
	
	for i in range(1,800):
		
		global cam_distance 
		if i<=300:
			print "static cam distacnce :",cam_distance
		if i>30 and i<500:
			cam_distance = 700 - i
			
		else:
			cam_distance =500
		
		print ("*************************")
		print "cam_distance : ",cam_distance
		
		print ("*************************")
		cruiseControl()
		
		time.sleep(0.1)
	
robot.init()

		
		
	
