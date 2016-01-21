from RobotCommunication import SerialCommands
import time

dist = int(raw_input('set distance/n'))
robot = SerialCommands('/dev/ttyAMA0',115200)
#robot.resetEncoders()
#old = robot.readEncoders()
#print old
#robot.autoCalibrate()
#time.sleep(5)
print robot.init()
robot.fixedDistance(dist)
#robot.startLineFollowing(40)



